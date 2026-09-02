import asyncio
from typing import List
from models.task import PlanStep
from agent.llm import generate_plan_from_goal

async def create_plan(goal: str) -> List[PlanStep]:
    """
    Uses the real LLM planner to parse the goal and return a structured plan.
    """
    return await generate_plan_from_goal(goal)
