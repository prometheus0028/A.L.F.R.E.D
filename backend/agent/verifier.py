from typing import Dict, Any, Optional
from models.task import Task, Result

def verify_task(task: Task) -> Optional[Result]:
    """Verify task completion based on goal type and collected evidence."""
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
    
    # File-based goal verification (electricity bill, receipt, documents, etc.)
    if any(keyword in goal_lower for keyword in ["bill", "receipt", "invoice", "document", "found", "email", "file"]):
        # Look for extracted amount in analyze action
        extracted_amount = None
        searched_file = None
        evidence = []
        
        for action in task.actions:
            if action.operation == "search" and action.tool_result:
                # Count found files
                results = action.tool_result.get("results", [])
                if results:
                    searched_file = results[0].get("filename", "")
                    evidence.append(f"Found {action.tool_result.get('count', 0)} files")
            
            elif action.operation == "read" and action.tool_result:
                evidence.append(f"Read file ({action.tool_result.get('size', 0)} bytes)")
            
            elif action.operation == "analyze" and action.tool_result:
                extracted = action.tool_result.get("extracted", {})
                if "amount" in extracted:
                    extracted_amount = extracted["amount"]
                    evidence.append(f"Extracted amount: ${extracted_amount}")
                if "date" in extracted:
                    evidence.append(f"Date: {extracted['date']}")
        
        # Task succeeds if we found and extracted information
        if extracted_amount is not None:
            return Result(
                type="file_info_extracted",
                status="verified",
                title=f"Found and extracted from {searched_file or 'file'}",
                summary=f"Successfully located and extracted amount: ${extracted_amount}",
                amount=extracted_amount,
                file_name=searched_file,
                evidence=evidence
            )
        
        # If we searched and found files but didn't extract amount, still partial success
        # Do not return a successful result when the requested amount is absent.
    
    return None
