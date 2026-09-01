from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import asyncio
from typing import Dict, Any, Optional
import datetime
from sse_starlette.sse import EventSourceResponse

from models.task import Task
from storage.database import save_task, get_task
from agent.planner import create_plan
from agent.executor import execute_task
from blockchain.adapter import submit_transaction

app = FastAPI(title="ALFRED Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GoalRequest(BaseModel):
    goal: str

class ApproveRequest(BaseModel):
    approval_id: str

class RejectRequest(BaseModel):
    approval_id: str
    reason: Optional[str] = None

# A simple in-memory queue per task for SSE events
task_event_queues: Dict[str, asyncio.Queue] = {}

async def emit_event(event_type: str, task_id: str, data: dict):
    event = {
        "type": event_type,
        "task_id": task_id,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "data": data
    }
    if task_id in task_event_queues:
        await task_event_queues[task_id].put(event)

@app.post("/api/tasks", status_code=201)
async def create_task_endpoint(request: GoalRequest):
    if not request.goal or not request.goal.strip():
        raise HTTPException(status_code=400, detail={"code": "INVALID_GOAL", "message": "A non-empty goal is required."})
        
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    
    task = Task(
        task_id=task_id,
        goal=request.goal,
        status="created"
    )
    save_task(task)
    
    # Initialize event queue
    task_event_queues[task_id] = asyncio.Queue()
    
    # Start task asynchronously
    asyncio.create_task(run_task(task))
    
    return {
        "task_id": task_id,
        "status": "created",
        "goal": request.goal
    }

async def run_task(task: Task):
    # Transition to planning
    task.status = "planning"
    save_task(task)
    await emit_event("goal_received", task.task_id, {"goal": task.goal})
    
    # Planning
    plan_steps = create_plan(task.goal)
    task.plan = plan_steps
    task.total_steps = len(plan_steps)
    task.status = "executing"
    save_task(task)
    
    await emit_event("plan_created", task.task_id, {"step_count": task.total_steps})
    
    # Start execution loop
    await execute_task(task, emit_event)
    save_task(task)

@app.get("/api/tasks/{task_id}")
async def get_task_endpoint(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
    return task

@app.get("/api/tasks/{task_id}/events")
async def task_events_endpoint(request: Request, task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
        
    if task_id not in task_event_queues:
        task_event_queues[task_id] = asyncio.Queue()
        
    async def event_generator():
        queue = task_event_queues[task_id]
        while True:
            if await request.is_disconnected():
                break
            
            try:
                # Wait for an event with a timeout
                event = await asyncio.wait_for(queue.get(), timeout=1.0)
                import json
                yield {
                    "event": event["type"],
                    "data": json.dumps(event)
                }
            except asyncio.TimeoutError:
                # Send a heartbeat or just continue
                continue
                
    return EventSourceResponse(event_generator())

@app.post("/api/tasks/{task_id}/approve")
async def approve_task_endpoint(task_id: str, request: ApproveRequest):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
        
    if task.status != "waiting_approval" or not task.approval or task.approval.approval_id != request.approval_id:
        raise HTTPException(status_code=400, detail={"code": "INVALID_STATE", "message": "Task is not waiting for this approval."})
        
    task.approval.status = "approved"
    task.status = "executing"
    save_task(task)
    
    # Actually submit the transaction now that it is approved
    tx_hash = submit_transaction({
        "vendor": task.approval.vendor,
        "amount": task.approval.amount
    })
    
    # Record transaction hash in action
    if task.actions and task.actions[-1].tool == "finance":
        task.actions[-1].summary = tx_hash
    
    # Resume task execution
    asyncio.create_task(resume_task(task))
    
    return {
        "task_id": task_id,
        "status": "executing",
        "message": "Approval accepted."
    }
    
async def resume_task(task: Task):
    # Continue from next step
    task.current_step += 1
    await execute_task(task, emit_event)
    save_task(task)

@app.post("/api/tasks/{task_id}/reject")
async def reject_task_endpoint(task_id: str, request: RejectRequest):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
        
    if task.status != "waiting_approval" or not task.approval or task.approval.approval_id != request.approval_id:
        raise HTTPException(status_code=400, detail={"code": "INVALID_STATE", "message": "Task is not waiting for this approval."})
        
    task.approval.status = "rejected"
    task.status = "failed"
    save_task(task)
    
    await emit_event("task_failed", task.task_id, {"summary": "Payment was rejected by the user."})
    
    reason = request.reason or "Payment was rejected by the user."
    return {
        "task_id": task_id,
        "status": "failed",
        "message": reason
    }
