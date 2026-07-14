"""
CRUD operations for FastAPI app
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Product, Customer, Order, OrderItem
from schemas import ProductCreate, ProductUpdate, CustomerCreate, CustomerUpdate, OrderCreate, OrderUpdate


# ==================== PRODUCT CRUD ====================

def create_product(db: Session, product: ProductCreate) -> Product:
    """Create a new product"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Product:
    """Get product by id"""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100, category: str = None) -> list:
    """Get all products with optional category filter"""
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    return query.offset(skip).limit(limit).all()


def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Product:
    """Update a product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Soft delete a product"""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    
    db_product.is_active = False
    db.commit()
    return True


# ==================== CUSTOMER CRUD ====================

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Create a new customer"""
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, customer_id: int) -> Customer:
    """Get customer by id"""
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> list:
    """Get all customers"""
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer_id: int, customer_update: CustomerUpdate) -> Customer:
    """Update a customer"""
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    
    update_data = customer_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, customer_id: int) -> bool:
    """Delete a customer"""
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return False
    
    db.delete(db_customer)
    db.commit()
    return True


# ==================== ORDER CRUD ====================

def create_order(db: Session, order: OrderCreate) -> Order:
    """Create a new order with items"""
    # Create order
    db_order = Order(
        customer_id=order.customer_id,
        shipping_address=order.shipping_address
    )
    db.add(db_order)
    db.flush()  # Get order id
    
    # Create order items
    total_amount = 0
    for item in order.items:
        db_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price
        )
        db.add(db_item)
        total_amount += item.quantity * item.unit_price
        
        # Update product stock
        product = get_product(db, item.product_id)
        if product:
            product.stock -= item.quantity
    
    db_order.total_amount = total_amount
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> Order:
    """Get order by id"""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100, customer_id: int = None) -> list:
    """Get all orders with optional customer filter"""
    query = db.query(Order)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    return query.offset(skip).limit(limit).all()


def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Order:
    """Update an order"""
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    
    update_data = order_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int) -> bool:
    """Delete an order"""
    db_order = get_order(db, order_id)
    if not db_order:
        return False
    
    db.delete(db_order)
    db.commit()
    return True
