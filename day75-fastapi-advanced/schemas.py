"""
Pydantic schemas for FastAPI app
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ==================== PRODUCT SCHEMAS ====================

class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    is_active: bool = True


class ProductCreate(ProductBase):
    """Product create schema"""
    pass


class ProductUpdate(BaseModel):
    """Product update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Product response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== CUSTOMER SCHEMAS ====================

class CustomerBase(BaseModel):
    """Base customer schema"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=50)


class CustomerCreate(CustomerBase):
    """Customer create schema"""
    pass


class CustomerUpdate(BaseModel):
    """Customer update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=50)


class CustomerResponse(CustomerBase):
    """Customer response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== ORDER SCHEMAS ====================

class OrderItemBase(BaseModel):
    """Order item base schema"""
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    """Order item create schema"""
    pass


class OrderItemResponse(OrderItemBase):
    """Order item response schema"""
    id: int
    order_id: int
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Order base schema"""
    customer_id: int
    status: str = "pending"
    shipping_address: Optional[str] = None


class OrderCreate(BaseModel):
    """Order create schema"""
    customer_id: int
    items: List[OrderItemCreate]
    shipping_address: Optional[str] = None


class OrderUpdate(BaseModel):
    """Order update schema"""
    status: Optional[str] = None
    shipping_address: Optional[str] = None


class OrderResponse(OrderBase):
    """Order response schema"""
    id: int
    order_date: datetime
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    customer: Optional[CustomerResponse] = None
    
    class Config:
        from_attributes = True
