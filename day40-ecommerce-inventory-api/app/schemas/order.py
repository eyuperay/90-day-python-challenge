from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    product_name: Optional[str] = None
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_email: EmailStr
    shipping_address: str = Field(..., min_length=1)

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]
    user_id: Optional[int] = None
    
    class Config:
        from_attributes = True