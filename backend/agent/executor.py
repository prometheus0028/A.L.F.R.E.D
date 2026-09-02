import asyncio
import uuid
import datetime
from typing import Dict, Any, Callable
from models.task import Task, Action, Approval, ApprovalPolicyInfo
from tools import finance
from blockchain.adapter import submit_transaction
from agent.tools import TOOL_REGISTRY

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
    
    try:
        if step.tool in TOOL_REGISTRY:
            tool_func = TOOL_REGISTRY[step.tool]
            kwargs = getattr(step, "tool_arguments", {})
            
            # Check if this tool has been approved by the user
            is_approved = False
            if task.approval and task.approval.status == "approved":
                is_approved = True
                
            # Only inject is_approved if the tool accepts it (to avoid breaking simple tools)
            import inspect
            if "is_approved" in inspect.signature(tool_func).parameters:
                kwargs["is_approved"] = is_approved
                
            result = await asyncio.to_thread(tool_func, user_id=task.user_id, **kwargs)
            
            if result.get("success"):
                if result.get("approval_required"):
                    task.status = "waiting_approval"
                    approval_data = result.get("approval", {})
                    approval = Approval(
                        approval_id=f"approval_{uuid.uuid4().hex[:8]}",
                        type=approval_data.get("type", "generic"),
                        title=approval_data.get("title", "Action requires approval"),
                        vendor=approval_data.get("vendor"),
                        amount=approval_data.get("amount"),
                        currency=approval_data.get("currency"),
                        invoice_id=approval_data.get("invoice_id"),
                        policy=ApprovalPolicyInfo(**approval_data.get("policy", {})) if "policy" in approval_data else None
                    )
                    task.approval = approval
                    await emit_event("approval_required", task.task_id, {"approval": approval.dict()})
                    success = True
                    summary = "Approval required"
                else:
                    success = True
                    summary = f"Executed {step.tool} successfully. Data snippet: {str(result.get('data', ''))[:500]}"
                    if is_approved:
                        task.approval = None
            else:
                success = False
                summary = f"Tool {step.tool} failed: {result.get('error')}"
        else:
            success = False
            summary = f"Unknown tool: {step.tool}"
    except Exception as e:
        success = False
        summary = f"Error: {str(e)}"
        
    action.status = "completed" if success else "failed"
    action.summary = summary
    await emit_event("tool_completed", task.task_id, {
        "tool": tool_module,
        "operation": tool_operation,
        "summary": summary,
        "success": success,
    })
    step.status = "completed" if success else "failed"
    await emit_event("step_completed", task.task_id, {"step_id": step.id, "success": success})
    return success



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
            
    task.status = "verifying"
    await emit_event("verification_started", task.task_id, {})
    from agent.verifier import verify_task
    result = await verify_task(task)
    
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


