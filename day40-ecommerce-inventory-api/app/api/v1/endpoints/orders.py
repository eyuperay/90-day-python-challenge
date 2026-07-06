from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse, OrderItemResponse

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = 0
    order_items_data = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Ürün {item.product_id} bulunamadı")
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail=f"{product.name} için yeterli stok yok")
        
        product.stock_quantity -= item.quantity
        total += item.price * item.quantity
        
        order_items_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        })
    
    db_order = Order(
        order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        shipping_address=order.shipping_address,
        total_amount=total,
        user_id=current_user.id
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item_data in order_items_data:
        db_item = OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.offset(skip).limit(limit).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    return order

@router.put("/{order_id}/status")
async def update_order_status(
    order_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sipariş bulunamadı")
    
    order.status = status
    db.commit()
    return {"message": "Sipariş durumu güncellendi", "status": status}