from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Dict, Any
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        is_active: Optional[bool] = None
    ):
        query = db.query(Product)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%")
                )
            )
        if category_id:
            query = query.filter(Product.category_id == category_id)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if is_active is not None:
            query = query.filter(Product.is_active == is_active)
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        return products, total
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str):
        return db.query(Product).filter(Product.sku == sku).first()
    
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate):
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product_data: ProductUpdate):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None
        
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return False
        
        db.delete(product)
        db.commit()
        return True