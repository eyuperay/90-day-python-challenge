from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InteractionBase(BaseModel):
    interaction_type: str = Field(..., pattern="^(call|email|meeting|note|task)$")
    subject: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class InteractionCreate(InteractionBase):
    customer_id: Optional[int] = None
    lead_id: Optional[int] = None

class InteractionResponse(InteractionBase):
    id: int
    interaction_type: str
    date: datetime
    created_at: datetime
    user_id: int
    user_name: Optional[str] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    lead_id: Optional[int] = None
    lead_name: Optional[str] = None
    
    class Config:
        from_attributes = True