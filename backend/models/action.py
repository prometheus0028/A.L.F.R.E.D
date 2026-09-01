from pydantic import BaseModel
from typing import Optional

class Action(BaseModel):
    id: str
    tool: str
    operation: str
    status: str = "pending"
    summary: Optional[str] = None
