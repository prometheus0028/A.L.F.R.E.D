import asyncio
import uuid
import datetime
from typing import Dict, Any, Callable
from models.task import Task, Action, Approval, ApprovalPolicyInfo
from tools import calendar, email, files, documents, finance
from blockchain.adapter import submit_transaction

async def execute_step(task: Task, step_index: int, emit_event: Callable) -> bool:
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
        if tool_module == "calendar" and tool_operation == "search":
            results = calendar.search()
            summary = f"Found {len(results)} events"
        elif tool_module == "email" and tool_operation == "search":
            results = email.search()
            summary = f"Found {len(results)} relevant emails"
        elif tool_module == "files" and tool_operation == "search":
            query = "Rahul project report" if step_index == 2 else "project status"
            results = files.search(query)
            if not results:
                success = False
                summary = "No exact result."
            else:
                summary = f"Found {len(results)} files"
        elif tool_module == "documents" and tool_operation == "create":
            documents.create("Meeting Briefing", "Briefing content...", "meeting_brief.md")
            summary = "Meeting briefing created"
        elif tool_module == "finance" and tool_operation == "list_pending_invoices":
            results = finance.list_pending_invoices()
            summary = f"Found {len(results)} invoices"
        elif tool_module == "finance" and tool_operation == "propose_payment":
            proposal = finance.propose_payment("INV-1042")
            if proposal.get("policy", {}).get("result") == "APPROVAL_REQUIRED":
                task.status = "waiting_approval"
                approval = Approval(
                    approval_id=f"approval_{uuid.uuid4().hex[:8]}",
                    type="payment", title="Payment requires approval",
                    vendor=proposal["vendor"], amount=proposal["amount"],
                    currency=proposal["currency"], invoice_id=proposal["invoice_id"],
                    policy=ApprovalPolicyInfo(**proposal["policy"])
                )
                task.approval = approval
                await emit_event("approval_required", task.task_id, {"approval": approval.dict()})
                success = True
                summary = "Approval required"
            else:
                summary = "Payment proposed"
        else:
            summary = f"Executed {step.tool}"
    except Exception as e:
        success = False
        summary = f"Error: {str(e)}"
        
    action.status = "completed" if success else "failed"
    action.summary = summary
    await emit_event("tool_completed", task.task_id, {"tool": tool_module, "operation": tool_operation, "summary": summary, "success": success})
    step.status = "completed" if success else "failed"
    await emit_event("step_completed", task.task_id, {"step_id": step.id, "success": success})
    return success

async def execute_task(task: Task, emit_event: Callable):
    while task.current_step < len(task.plan):
        if task.status == "waiting_approval":
            return
        success = await execute_step(task, task.current_step, emit_event)
        if task.status == "waiting_approval":
            return
        if not success:
            task.status = "replanning"
            failed_action = task.actions[-1]
            await emit_event("replanning", task.task_id, {"reason": failed_action.summary, "attempt": 1, "message": "Generating alternative plan"})
            from agent.replanner import replan
            new_steps = replan(task.goal, failed_action)
            if new_steps:
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
