import asyncio
import uuid
import datetime
from typing import Dict, Any, Callable
from models.task import Task, Action, Approval, ApprovalPolicyInfo
from tools import calendar, email, files, documents, finance
from tools.tool_registry import get_operation
from blockchain.adapter import submit_transaction

async def execute_step(task: Task, step_index: int, emit_event: Callable) -> bool:
    """
    Execute a single plan step.
    Dynamically dispatches to tools based on registry.
    Handles delete confirmations and verifies mutations.
    Chains results from previous steps to next step params.
    """
    if step_index >= len(task.plan):
        return True
    step = task.plan[step_index]
    step.status = "running"
    await emit_event("step_started", task.task_id, {"step_id": step.id, "description": step.description})
    
    tool_parts = step.tool.split(".")
    tool_module = tool_parts[0]
    tool_operation = tool_parts[1] if len(tool_parts) > 1 else "run"
    
    action_id = f"action_{uuid.uuid4().hex[:8]}"
    action = Action(id=action_id, tool=tool_module, operation=tool_operation, status="running")
    task.actions.append(action)
    await emit_event("tool_started", task.task_id, {"tool": tool_module, "operation": tool_operation})
    
    success = True
    summary = ""
    tool_result = None
    
    try:
        # Before dispatch: substitute previous results into step params if needed
        step_params = step.params.copy() if step.params else {}
        
        # If this step needs a path from a previous search result
        if tool_module == "files" and tool_operation == "read" and not step_params.get("path"):
            # Look for previous search results
            for prev_action in task.actions[:-1]:  # Exclude current action
                if prev_action.tool_result and isinstance(prev_action.tool_result, dict):
                    results = prev_action.tool_result.get("results", [])
                    if results and len(results) > 0:
                        # Use the first (most relevant) result
                        step_params["path"] = results[0].get("path", "")
                        break
        
        # If this step needs content from a previous read result
        if tool_module == "files" and tool_operation == "analyze" and not step_params.get("content"):
            # Look for previous read results
            for prev_action in task.actions[:-1]:  # Exclude current action
                if prev_action.tool_result and isinstance(prev_action.tool_result, dict):
                    content = prev_action.tool_result.get("content")
                    if content:
                        step_params["content"] = content
                        break
        
        # Dynamic tool dispatch via registry
        tool_result = _dispatch_tool(tool_module, tool_operation, step, step_params)
        
        if tool_result is None:
            success = False
            summary = f"Tool not found: {step.tool}"
        elif isinstance(tool_result, dict) and tool_result.get("error"):
            success = False
            summary = tool_result.get("error", "Tool error")
        elif isinstance(tool_result, dict) and tool_result.get("confirmation_required"):
            # Delete confirmation flow
            task.status = "waiting_confirmation"
            task.pending_confirmation = {
                "type": "delete",
                "tool": tool_module,
                "operation": tool_operation,
                "path": tool_result.get("path"),
                "message": tool_result.get("message"),
            }
            await emit_event("confirmation_required", task.task_id, {
                "type": "delete",
                "path": tool_result.get("path"),
                "message": tool_result.get("message"),
            })
            success = True  # Step "succeeds" (awaiting confirmation)
            summary = f"Delete confirmation required for {tool_result.get('path')}"
        else:
            # Verify mutation if it's a write operation
            if tool_operation in ("create", "write", "append", "copy", "move", "rename"):
                if isinstance(tool_result, dict) and tool_result.get("verified"):
                    summary = f"{tool_operation.capitalize()} successful (verified)"
                else:
                    success = False
                    summary = f"{tool_operation.capitalize()} failed verification"
            elif isinstance(tool_result, dict) and "results" in tool_result:
                count = tool_result.get("count", 0)
                summary = f"Found {count} files" if count > 0 else "No files found"
                success = count > 0
            elif isinstance(tool_result, dict) and "count" in tool_result:
                summary = f"Listed {tool_result.get('count', 0)} items"
            elif isinstance(tool_result, dict) and "content" in tool_result:
                summary = f"Read {tool_result.get('size', 0)} bytes"
            elif tool_operation == "analyze":
                # Analysis result
                summary = tool_result.get("summary", "Analysis complete")
            else:
                summary = f"Executed {step.tool}"
    except Exception as e:
        success = False
        summary = f"Error: {str(e)}"
        
    action.status = "completed" if success else "failed"
    action.summary = summary
    action.tool_result = tool_result  # Store result for verification and chaining
    await emit_event("tool_completed", task.task_id, {
        "tool": tool_module,
        "operation": tool_operation,
        "summary": summary,
        "success": success,
    })
    step.status = "completed" if success else "failed"
    await emit_event("step_completed", task.task_id, {"step_id": step.id, "success": success})
    return success

def _dispatch_tool(tool_module: str, tool_operation: str, step: Any, step_params: Dict[str, Any] = None) -> Any:
    """
    Dynamically dispatch to tool operations.
    step_params can override/augment step.params (used for result chaining).
    """
    if step_params is None:
        step_params = {}
    
    try:
        if tool_module == "calendar" and tool_operation == "search":
            return calendar.search()
        
        elif tool_module == "email" and tool_operation == "search":
            return email.search()
        
        elif tool_module == "files" and tool_operation == "search":
            query = step_params.get("query", "")
            path = step_params.get("path", ".")
            file_type = step_params.get("file_type")
            return files.search(query, path, file_type)
        
        elif tool_module == "files" and tool_operation == "read":
            path = step_params.get("path", "")
            return files.read(path)
        
        elif tool_module == "files" and tool_operation == "list":
            path = step_params.get("path", ".")
            return files.list(path)
        
        elif tool_module == "files" and tool_operation == "create":
            path = step_params.get("path", "")
            content = step_params.get("content", "")
            return files.create(path, content)
        
        elif tool_module == "files" and tool_operation == "write":
            path = step_params.get("path", "")
            content = step_params.get("content", "")
            return files.write(path, content)
        
        elif tool_module == "files" and tool_operation == "append":
            path = step_params.get("path", "")
            content = step_params.get("content", "")
            return files.append(path, content)
        
        elif tool_module == "files" and tool_operation == "copy":
            source = step_params.get("source", "")
            destination = step_params.get("destination", "")
            return files.copy(source, destination)
        
        elif tool_module == "files" and tool_operation == "move":
            source = step_params.get("source", "")
            destination = step_params.get("destination", "")
            return files.move(source, destination)
        
        elif tool_module == "files" and tool_operation == "rename":
            path = step_params.get("path", "")
            new_name = step_params.get("new_name", "")
            return files.rename(path, new_name)
        
        elif tool_module == "files" and tool_operation == "delete":
            path = step_params.get("path", "")
            return files.delete(path)
        
        elif tool_module == "files" and tool_operation == "analyze":
            # Pseudo-tool: extract information from content
            content = step_params.get("content", "")
            return _analyze_content(content)
        
        elif tool_module == "documents" and tool_operation == "create":
            return documents.create("Meeting Briefing", "Briefing content...", "meeting_brief.md")
        
        elif tool_module == "finance" and tool_operation == "list_pending_invoices":
            return finance.list_pending_invoices()
        
        elif tool_module == "finance" and tool_operation == "propose_payment":
            return finance.propose_payment("INV-1042")
        
        else:
            return {"error": f"Unknown tool: {tool_module}.{tool_operation}"}
    except Exception as e:
        return {"error": str(e)}

async def execute_task(task: Task, emit_event: Callable):
    replan_attempts = 0
    while task.current_step < len(task.plan):
        if task.status in ("waiting_approval", "waiting_confirmation"):
            return
        success = await execute_step(task, task.current_step, emit_event)
        if task.status in ("waiting_approval", "waiting_confirmation"):
            return
        if not success:
            task.status = "replanning"
            failed_action = task.actions[-1]
            replan_attempts += 1
            await emit_event("replanning", task.task_id, {
                "reason": failed_action.summary,
                "attempt": replan_attempts,
                "message": "Generating alternative plan"
            })
            from agent.replanner import replan
            new_steps = replan(task.goal, failed_action)
            if new_steps and replan_attempts <= 1:
                task.plan = task.plan[:task.current_step] + new_steps
                task.total_steps = len(task.plan)
                task.status = "executing"
            else:
                task.status = "failed"
                await emit_event("task_failed", task.task_id, {"summary": "Replanning failed"})
                return
        else:
            task.current_step += 1
            
        await asyncio.sleep(0.5)
            
    task.status = "verifying"
    await emit_event("verification_started", task.task_id, {})
    from agent.verifier import verify_task
    result = verify_task(task)
    
    if result:
        task.result = result
        task.status = "completed"
        await emit_event("verification_passed", task.task_id, {})
        await emit_event("task_completed", task.task_id, {"summary": result.summary})
    else:
        task.status = "failed"
        await emit_event("verification_failed", task.task_id, {})
        await emit_event("task_failed", task.task_id, {"summary": "Verification failed"})

async def confirm_deletion(task: Task, emit_event: Callable) -> bool:
    """
    Confirm a pending delete operation.
    Execute the delete, verify, and continue task execution.
    """
    if not getattr(task, "pending_confirmation", None):
        return False
    
    conf = task.pending_confirmation
    if conf.get("type") != "delete":
        return False
    
    path = conf.get("path")
    
    try:
        result = files.delete_confirmed(path)
        
        if result.get("verified"):
            await emit_event("confirmation_executed", task.task_id, {
                "type": "delete",
                "path": path,
                "status": "deleted",
            })
            task.pending_confirmation = None
            task.status = "executing"
            return True
        else:
            await emit_event("confirmation_failed", task.task_id, {
                "type": "delete",
                "path": path,
                "error": result.get("error", "Unknown error"),
            })
            task.pending_confirmation = None
            task.status = "failed"
            return False
    except Exception as e:
        await emit_event("confirmation_failed", task.task_id, {
            "type": "delete",
            "path": path,
            "error": str(e),
        })
        task.pending_confirmation = None
        task.status = "failed"
        return False

def _analyze_content(content: str) -> Dict[str, Any]:
    """
    Pseudo-tool: Extract key information from content.
    For electricity bills, looks for amounts, dates, etc.
    """
    import re
    
    if not content:
        return {"error": "No content provided"}
    
    result = {
        "summary": "Content analyzed",
        "extracted": {}
    }
    
    # Look for currency amounts (dollar, euro, rupees, etc.)
    # Prefer amounts near billing labels before considering other currencies.
    amount_patterns = [
        r'(?i)(?:total\s+amount\s+due|amount\s+paid|amount|total|due|paid)[:\s]*[$€₹]?([\d,]+\.?\d*)',
        r'[$€₹]([\d,]+\.?\d*)',
    ]
    
    for pattern in amount_patterns:
        matches = re.findall(pattern, content)
        if matches:
            # Take the first/most likely match
            amount_str = matches[0]
            if isinstance(amount_str, tuple):
                amount_str = amount_str[-1]
            # Remove commas and convert to float
            try:
                amount = float(amount_str.replace(',', ''))
                result["extracted"]["amount"] = amount
                break
            except:
                pass
    
    # Look for dates
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',  # MM/DD/YYYY
        r'\d{1,2}-\d{1,2}-\d{2,4}',  # MM-DD-YYYY
        r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, content)
        if matches:
            result["extracted"]["date"] = matches[0]
            break
    
    if result["extracted"]:
        result["summary"] = f"Extracted: {len(result['extracted'])} items"
    
    return result
