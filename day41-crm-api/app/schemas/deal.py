from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DealBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    stage: Optional[str] = "prospecting"
    probability: Optional[int] = Field(0, ge=0, le=100)
    expected_close_date: Optional[datetime] = None
    description: Optional[str] = None

class DealCreate(DealBase):
    customer_id: int

class DealUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = None
    stage: Optional[str] = None
    probability: Optional[int] = None
    expected_close_date: Optional[datetime] = None
    actual_close_date: Optional[datetime] = None
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None

class DealResponse(DealBase):
    id: int
    stage: str
    probability: int
    customer_id: int
    customer_name: Optional[str] = None
    assigned_to_id: Optional[int]
    assigned_to_name: Optional[str] = None
    expected_close_date: Optional[datetime]
    actual_close_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True