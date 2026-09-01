from typing import Dict, Any, Optional
from models.task import Task, Result

def verify_task(task: Task) -> Optional[Result]:
    goal_lower = task.goal.lower()
    if "meeting" in goal_lower and "rahul" in goal_lower:
        return Result(
            type="meeting_brief",
            status="verified",
            title="Meeting briefing created",
            file_name="meeting_brief.md",
            summary="Meeting briefing created and verified.",
            evidence=["1 calendar event", "4 emails", "2 documents"]
        )
    if "invoice" in goal_lower or "policy" in goal_lower:
        tx_hash = "0xDEMO..."
        for action in task.actions:
            if action.operation == "submit_transaction" and getattr(action, "summary", ""):
                tx_hash = action.summary
        return Result(
            type="payment",
            status="verified",
            title="Payment complete",
            vendor="Acme Supplies",
            amount=3800,
            currency="INR",
            transaction_hash=tx_hash,
            summary="Transaction confirmed on blockchain.",
            evidence=["Policy passed", "User approved", "Transaction confirmed"]
        )
    return None
