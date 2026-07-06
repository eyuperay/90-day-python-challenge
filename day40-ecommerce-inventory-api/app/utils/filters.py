from typing import Optional
from pydantic import BaseModel

class ProductFilter(BaseModel):
    search: Optional[str] = None
    category_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    is_active: Optional[bool] = None

class OrderFilter(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None