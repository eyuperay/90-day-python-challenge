from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "pending"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assigned_to_id: int
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    priority: str
    status: str
    assigned_to_id: int
    assigned_to_name: Optional[str] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    lead_id: Optional[int] = None
    lead_name: Optional[str] = None
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True