from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
import uuid
import asyncio
from typing import Dict, Any, Optional
import datetime
from sse_starlette.sse import EventSourceResponse
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
import tempfile
import os
import wave
import io
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

from auth.google import router as google_router
from models.task import Task
from storage.database import save_task, get_task
from agent.planner import create_plan
from agent.executor import execute_task
from blockchain.adapter import submit_transaction

app = FastAPI(title="ALFRED Backend")
app.include_router(google_router)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret"),
    same_site="lax",
    https_only=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
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

whisper_model = None
piper_voice = None

@app.post("/api/speech/transcribe")
async def transcribe_speech(audio: UploadFile = File(...)):
    global whisper_model
    if whisper_model is None:
        from faster_whisper import WhisperModel
        whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
        
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name
        
    try:
        segments, info = whisper_model.transcribe(tmp_path, beam_size=1)
        text = " ".join([segment.text for segment in segments])
        return {"text": text.strip()}
    finally:
        os.unlink(tmp_path)

class SynthesizeRequest(BaseModel):
    text: str

@app.post("/api/speech/synthesize")
async def synthesize_speech(request: SynthesizeRequest):
    global piper_voice
    if piper_voice is None:
        from piper import PiperVoice
        model_path = os.path.join(os.path.dirname(__file__), "models", "en_US-lessac-low.onnx")
        config_path = os.path.join(os.path.dirname(__file__), "models", "en_US-lessac-low.onnx.json")
        piper_voice = PiperVoice.load(model_path, config_path)
        
    import wave
    import io
    wav_io = io.BytesIO()
    with wave.open(wav_io, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(piper_voice.config.sample_rate)
        piper_voice.synthesize_wav(request.text, wav_file)
        
    wav_io.seek(0)
    return StreamingResponse(wav_io, media_type="audio/wav")

@app.post("/api/files/upload")
async def upload_file_endpoint(file: UploadFile = File(...)):
    from tools.files import write as write_file
    try:
        content = await file.read()
        
        # Files write takes a string, but the content is bytes
        # We need to decode it for write, or use append which takes str but encodes to bytes
        # Wait, the tools.files.write function does: f.write(content) with encoding="utf-8"
        # So we should decode to string if it's text, but for binary files (PDF) it will fail.
        # Looking at tools.files, append uses binary write: f.write(content.encode("utf-8")) if it's str
        # Actually let's just write it manually using ALFRED_WORKSPACE_ROOT to be 100% binary safe
        from tools.files import _normalize_path
        
        # This resolves and validates the path is inside workspace
        file_path = _normalize_path(file.filename)
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
            
        return {
            "success": True,
            "file": {
                "name": file.filename,
                "path": file.filename,
                "size": len(content),
                "type": file.content_type
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail={"error": str(e)})

@app.get("/api/files")
async def list_files_endpoint():
    from tools.files import list as list_files
    result = list_files(".")
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@app.get("/api/files/{filename:path}")
async def get_file_endpoint(filename: str):
    from tools.files import _normalize_path
    from fastapi.responses import FileResponse
    try:
        file_path = _normalize_path(filename)
        if not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        return FileResponse(file_path)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/files/{filename:path}")
async def delete_file_endpoint(filename: str):
    from tools.files import delete_confirmed
    try:
        result = delete_confirmed(filename)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return {"success": True, "message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/tasks", status_code=201)
async def create_task_endpoint(request: Request, body: GoalRequest):
    user = request.session.get("google_user")
    if not user:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "You must be logged in to create a task."})

    if not body.goal or not body.goal.strip():
        raise HTTPException(status_code=400, detail={"code": "INVALID_GOAL", "message": "A non-empty goal is required."})
        
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    
    task = Task(
        task_id=task_id,
        user_id=user["sub"],
        goal=body.goal,
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
        "goal": body.goal
    }

@app.get("/api/tasks")
async def get_all_tasks_endpoint(request: Request):
    user = request.session.get("google_user")
    if not user:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHORIZED", "message": "You must be logged in."})
    
    from storage.database import _tasks
    tasks = [t for t in _tasks.values() if getattr(t, "user_id", None) == user["sub"]]
    # Sort by creation time if we had it, but for now just reverse list so newest is first
    return list(reversed(tasks))

async def run_task(task: Task):
    # Transition to planning
    task.status = "planning"
    save_task(task)
    await emit_event("goal_received", task.task_id, {"goal": task.goal})
    
    # Planning
    plan_steps = await create_plan(task.goal)
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
    
    # Resume task execution on the SAME step to execute the side-effect
    asyncio.create_task(resume_task_same_step(task))
    
    return {
        "task_id": task_id,
        "status": "executing",
        "message": "Approval accepted."
    }
    
async def resume_task_same_step(task: Task):
    # Do NOT increment step, execute the same tool again with is_approved=True
    await execute_task(task, emit_event)
    save_task(task)

async def resume_task(task: Task):
    # Continue from next step (used by delete confirmation)
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

@app.post("/api/tasks/{task_id}/confirm-delete")
async def confirm_delete_endpoint(task_id: str):
    """Confirm a pending file deletion."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
    
    if task.status != "waiting_confirmation" or not task.pending_confirmation:
        raise HTTPException(status_code=400, detail={"code": "INVALID_STATE", "message": "Task is not waiting for deletion confirmation."})
    
    # Confirm and continue execution
    from agent.executor import confirm_deletion
    success = await confirm_deletion(task, emit_event)
    save_task(task)
    
    if success:
        # Resume task execution
        asyncio.create_task(resume_task(task))
        
        return {
            "task_id": task_id,
            "status": "executing",
            "message": "Deletion confirmed, resuming task."
        }
    else:
        return {
            "task_id": task_id,
            "status": "failed",
            "message": "Deletion confirmation failed."
        }

@app.post("/api/tasks/{task_id}/reject-delete")
async def reject_delete_endpoint(task_id: str, request: RejectRequest):
    """Reject a pending file deletion."""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found."})
    
    if task.status != "waiting_confirmation" or not task.pending_confirmation:
        raise HTTPException(status_code=400, detail={"code": "INVALID_STATE", "message": "Task is not waiting for deletion confirmation."})
    
    task.pending_confirmation = None
    task.status = "failed"
    save_task(task)
    
    await emit_event("task_failed", task.task_id, {"summary": "File deletion was rejected by the user."})
    
    reason = request.reason or "File deletion was rejected by the user."
    return {
        "task_id": task_id,
        "status": "failed",
        "message": reason
    }
