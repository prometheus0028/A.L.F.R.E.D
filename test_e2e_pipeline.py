#!/usr/bin/env python3
"""
End-to-end test for the ALFRED agent pipeline.
Tests the complete flow: goal -> plan -> execute -> verify
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Setup path for imports
sys.path.insert(0, '/Users/Aarav/Documents/GitHub/A.L.F.R.E.D/backend')

from models.task import Task
from agent.planner import create_plan
from agent.executor import execute_task
from agent.verifier import verify_task
from storage.database import save_task, get_task
from tools import files
from typing import Dict, Any

files.ALFRED_WORKSPACE_ROOT = Path(__file__).parent / "demo_data"

# Mock emit_event function for testing
emitted_events = []

async def mock_emit_event(event_type: str, task_id: str, data: Dict[str, Any]):
    """Mock event emitter for testing."""
    emitted_events.append({
        "event": event_type,
        "task_id": task_id,
        "data": data,
        "timestamp": datetime.now().isoformat()
    })
    print(f"  [{event_type}] {data.get('summary', data.get('description', ''))}")

async def run_e2e_test(goal: str, test_name: str) -> Dict[str, Any]:
    """Run a complete end-to-end test."""
    print(f"\n{'='*70}")
    print(f"E2E TEST: {test_name}")
    print(f"{'='*70}")
    print(f"Goal: {goal}\n")
    
    # Create task
    task = Task(
        task_id=f"test_{datetime.now().timestamp()}",
        goal=goal,
        user_id="test_user",
    )
    
    print("1. PLANNING")
    print("-" * 70)
    # Plan
    plan = create_plan(goal)
    task.plan = plan
    task.total_steps = len(plan)
    
    print(f"   Generated {len(plan)} steps:")
    for i, step in enumerate(plan, 1):
        params_str = f"params={step.params}" if step.params else "params={}"
        print(f"   {i}. {step.description}")
        print(f"      tool: {step.tool}")
        print(f"      {params_str}")
    
    # Save initial task
    save_task(task)
    
    print("\n2. EXECUTING")
    print("-" * 70)
    emitted_events.clear()
    
    # Execute
    await execute_task(task, mock_emit_event)
    
    print(f"\n   Task status: {task.status}")
    print(f"   Current step: {task.current_step} / {task.total_steps}")
    print(f"   Total actions: {len(task.actions)}")
    
    # Print action details
    print("\n   Actions executed:")
    for i, action in enumerate(task.actions, 1):
        result_str = ""
        if action.tool_result:
            if isinstance(action.tool_result, dict):
                if "count" in action.tool_result:
                    result_str = f"({action.tool_result['count']} results)"
                elif "size" in action.tool_result:
                    result_str = f"({action.tool_result['size']} bytes)"
                elif "extracted" in action.tool_result:
                    extracted = action.tool_result["extracted"]
                    result_str = f"(extracted: {list(extracted.keys())})"
        print(f"   {i}. {action.tool}.{action.operation} - {action.status} {result_str}")
        if action.summary:
            print(f"      {action.summary}")
    
    print("\n3. VERIFYING")
    print("-" * 70)
    
    # Verify
    result = verify_task(task)
    task.result = result
    
    if result:
        print(f"   [PASS] Verification PASSED")
        print(f"   Title: {result.title}")
        print(f"   Status: {result.status}")
        print(f"   Summary: {result.summary}")
        if hasattr(result, 'amount') and result.amount:
            print(f"   Amount: ${result.amount}")
        if result.evidence:
            print(f"   Evidence:")
            for evidence in result.evidence:
                print(f"     - {evidence}")
    else:
        print(f"   [FAIL] Verification FAILED")
    
    # Return results
    # Return results
    verified = bool(result and result.status == "verified" and task.status == "completed")
    return {
        "goal": goal,
        "test_name": test_name,
        "success": verified,
        "task_status": task.status,
        "verification": verified,
        "actions": len(task.actions),
        "result": result,
        "task": task
    }

async def main():
    """Run the primary end-to-end task regression test."""
    print("\n" + "="*70)
    print("ALFRED AGENT PIPELINE - END-TO-END TESTS")
    print("="*70)
    
    results = []

    test1_result = await run_e2e_test(
        "Find the electricity bill I downloaded this month and tell me how much I paid.",
        "Electricity Bill Search and Extract"
    )
    results.append(test1_result)

    assert test1_result["success"], "Task did not complete with a verified result"
    assert len(test1_result["task"].plan) == 3
    assert test1_result["task"].plan[0].params["query"] == "electricity bill"
    assert test1_result["task"].actions[1].tool_result["path"] == "electricity_bill_jan_2024.txt"
    assert test1_result["result"].amount == 145
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for r in results if r["verification"])
    
    print(f"Total Tests: {total}")
    print(f"Passed Verification: {passed}/{total}")
    
    for result in results:
        status = "[PASS]" if result["verification"] else "[FAIL]"
        print(f"\n{status} - {result['test_name']}")
        print(f"      Status: {result['task_status']}")
        print(f"      Steps: {result['actions']}")
        if result['result']:
            print(f"      Result: {result['result'].summary}")
    
    print("\n" + "="*70)
    
    # Return success if at least first test passed
    return results[0]["verification"]

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
