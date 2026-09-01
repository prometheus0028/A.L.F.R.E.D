from typing import Dict, Any, List
from models.task import PlanStep

def create_plan(goal: str) -> List[PlanStep]:
    """Mock LLM planner that parses the goal and returns a structured plan."""
    goal_lower = goal.lower()
    
    if "meeting" in goal_lower and "rahul" in goal_lower:
        return [
            PlanStep(id="step_1", description="Find tomorrow's meeting with Rahul", tool="calendar.search", success_criteria=["meeting_found"]),
            PlanStep(id="step_2", description="Find relevant emails", tool="email.search", success_criteria=["emails_found"]),
            PlanStep(id="step_3", description="Find latest project document", tool="files.search", success_criteria=["document_found"]),
            PlanStep(id="step_4", description="Generate meeting briefing", tool="documents.create", success_criteria=["briefing_created"])
        ]
        
    if "invoice" in goal_lower or "policy" in goal_lower:
        return [
            PlanStep(id="step_1", description="Find pending invoice", tool="finance.list_pending_invoices", success_criteria=["invoice_found"]),
            PlanStep(id="step_2", description="Propose payment and check policy", tool="finance.propose_payment", success_criteria=["policy_checked", "approval_requested"])
        ]
        
    return [PlanStep(id="step_1", description="Analyze goal", tool="files.search", success_criteria=["analyzed"])]
