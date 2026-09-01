from typing import List, Dict, Any
from models.task import PlanStep, Action

def replan(goal: str, failed_action: Action) -> List[PlanStep]:
    if failed_action.tool == "files" and failed_action.operation == "search":
        return [
            PlanStep(id="step_3_alt", description="Search project status documents", tool="files.search", success_criteria=["document_found"]),
            PlanStep(id="step_4", description="Generate meeting briefing", tool="documents.create", success_criteria=["briefing_created"])
        ]
    return []
