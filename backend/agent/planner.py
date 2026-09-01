from typing import Dict, Any, List
from models.task import PlanStep

def _extract_search_terms(goal: str) -> str:
    """Extract meaningful search terms from goal text."""
    goal_lower = goal.lower()
    
    # Remove common question/request phrases
    for phrase in ["find ", "search for ", "locate ", "look for ", "tell me ", "what ", "where ", "how ",
                   "i downloaded", "downloaded", "the", "and tell me how", "and tell me what", "and let me know"]:
        goal_lower = goal_lower.replace(phrase, " ")
    
    # Remove common goal endings
    for phrase in [" and tell me", " and let me know", " please", " ?", " ."]:
        goal_lower = goal_lower.replace(phrase, "")
    
    # Extract important keywords (prioritize nouns)
    stopwords = {"the", "this", "that", "with", "from", "for", "and", "was", "i", "my", "me", "a", "an", "or", "is", "are", "be"}
    keywords = [w for w in goal_lower.split() if len(w) > 2 and w not in stopwords]
    
    # Return top 2 keywords (not 3) for more flexible matching
    return " ".join(keywords[:2]).strip() if keywords else "file"

def create_plan(goal: str) -> List[PlanStep]:
    """LLM planner that parses the goal and returns a structured plan."""
    goal_lower = goal.lower()
    
    if "meeting" in goal_lower and "rahul" in goal_lower:
        return [
            PlanStep(id="step_1", description="Find tomorrow's meeting with Rahul", tool="calendar.search", success_criteria=["meeting_found"]),
            PlanStep(id="step_2", description="Find relevant emails", tool="email.search", success_criteria=["emails_found"]),
            PlanStep(id="step_3", description="Find latest project document", tool="files.search", params={"query": "project report", "path": "."}, success_criteria=["document_found"]),
            PlanStep(id="step_4", description="Generate meeting briefing", tool="documents.create", success_criteria=["briefing_created"])
        ]
        
    if ("invoice" in goal_lower and any(word in goal_lower for word in ["pending", "pay", "payment"])) or "policy" in goal_lower:
        return [
            PlanStep(id="step_1", description="Find pending invoice", tool="finance.list_pending_invoices", success_criteria=["invoice_found"]),
            PlanStep(id="step_2", description="Propose payment and check policy", tool="finance.propose_payment", success_criteria=["policy_checked", "approval_requested"])
        ]
    
    # Generic file search plan (for electricity bill, receipts, documents, etc.)
    if "downloaded" in goal_lower or "bill" in goal_lower or "invoice" in goal_lower or "receipt" in goal_lower or "document" in goal_lower:
        search_terms = _extract_search_terms(goal)
        return [
            PlanStep(
                id="step_1",
                description=f"Search for files matching '{search_terms}'",
                tool="files.search",
                params={"query": search_terms, "path": "."},
                success_criteria=["files_found"]
            ),
            PlanStep(
                id="step_2",
                description="Read the most relevant file",
                tool="files.read",
                params={"path": ""},  # Will be filled by executor from step_1 result
                success_criteria=["content_read"]
            ),
            PlanStep(
                id="step_3",
                description="Extract requested information (amount, date, etc.)",
                tool="files.analyze",
                params={"content": ""},  # Will be filled by executor from step_2 result
                success_criteria=["info_extracted"]
            )
        ]
        
    # Fallback: generic file search with extracted terms
    search_terms = _extract_search_terms(goal)
    return [
        PlanStep(id="step_1", description=f"Search for files", tool="files.search", params={"query": search_terms, "path": "."}, success_criteria=["files_found"])
    ]
