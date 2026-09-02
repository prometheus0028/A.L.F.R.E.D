from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from .action import Action

class PlanStep(BaseModel):
    id: str
    description: str
    tool: str
    tool_arguments: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    success_criteria: List[str] = Field(default_factory=list)
    params: Dict[str, Any] = Field(default_factory=dict)  # For tool parameters

class ApprovalPolicyInfo(BaseModel):
    result: str
    vendor_approved: bool
    within_limit: bool
    limit: int

class Approval(BaseModel):
    approval_id: str
    type: str
    status: str = "pending"
    title: str
    vendor: str
    amount: int
    currency: str
    invoice_id: str
    policy: ApprovalPolicyInfo

class Result(BaseModel):
    type: str
    status: str
    title: Optional[str] = None
    file_name: Optional[str] = None
    summary: str
    evidence: List[str] = Field(default_factory=list)
    vendor: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None
    transaction_hash: Optional[str] = None

class Task(BaseModel):
    task_id: str
    user_id: Optional[str] = None
    goal: str
    status: str = "created"
    current_step: int = 0
    total_steps: int = 0
    plan: List[PlanStep] = Field(default_factory=list)
    actions: List[Action] = Field(default_factory=list)
    approval: Optional[Approval] = None
    pending_confirmation: Optional[Dict[str, Any]] = None  # For delete confirmations
    result: Optional[Result] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
