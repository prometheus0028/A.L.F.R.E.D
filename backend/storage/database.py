from typing import Dict, List, Optional
from models.task import Task

# In-memory dictionary for tasks for the MVP
_tasks: Dict[str, Task] = {}

def get_task(task_id: str) -> Optional[Task]:
    return _tasks.get(task_id)

def save_task(task: Task) -> None:
    _tasks[task.task_id] = task

def list_tasks() -> List[Task]:
    return list(_tasks.values())
