from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventoryBase(BaseModel):
    product_id: int
    quantity: int = 0
    reserved_quantity: int = 0
    reorder_point: int = 10

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[int] = None
    reserved_quantity: Optional[int] = None
    reorder_point: Optional[int] = None

class InventoryResponse(InventoryBase):
    id: int
    available_quantity: int
    last_updated: Optional[datetime]
    product_name: Optional[str] = None
    
    class Config:
        from_attributes = True