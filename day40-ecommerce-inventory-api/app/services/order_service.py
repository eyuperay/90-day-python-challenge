from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate

class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: Optional[int] = None):
        total = 0
        items = []
        
        for item in order_data.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise ValueError(f"Ürün {item.product_id} bulunamadı")
            
            if product.stock_quantity < item.quantity:
                raise ValueError(f"{product.name} için yeterli stok yok")
            
            product.stock_quantity -= item.quantity
            total += item.price * item.quantity
            
            items.append({
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price
            })
        
        db_order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            customer_name=order_data.customer_name,
            customer_email=order_data.customer_email,
            shipping_address=order_data.shipping_address,
            total_amount=total,
            user_id=user_id
        )
        
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        
        for item_data in items:
            db_item = OrderItem(
                order_id=db_order.id,
                **item_data
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_order)
        
        return db_order
    
    @staticmethod
    def get_orders(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
        query = db.query(Order)
        if status:
            query = query.filter(Order.status == status)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_order_by_id(db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, status: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return None
        order.status = status
        db.commit()
        return order