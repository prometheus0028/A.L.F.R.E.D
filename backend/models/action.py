from pydantic import BaseModel
from typing import Optional, Any

class Action(BaseModel):
    id: str
    tool: str
    operation: str
    status: str = "pending"
    summary: Optional[str] = None
    tool_result: Optional[Any] = None  # Store tool output for verification
