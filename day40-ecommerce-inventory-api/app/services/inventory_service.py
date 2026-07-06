from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.inventory import Inventory, InventoryLog, InventoryAction
from app.models.product import Product

class InventoryService:
    @staticmethod
    def get_inventory(db: Session, skip: int = 0, limit: int = 100, product_id: Optional[int] = None):
        query = db.query(Inventory)
        if product_id:
            query = query.filter(Inventory.product_id == product_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_inventory_by_product(db: Session, product_id: int):
        return db.query(Inventory).filter(Inventory.product_id == product_id).first()
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity_change: int, user_id: int, notes: str = ""):
        inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
        if not inventory:
            return None
        
        old_quantity = inventory.quantity
        inventory.quantity += quantity_change
        inventory.available_quantity = inventory.quantity - inventory.reserved_quantity
        
        db.commit()
        
        log = InventoryLog(
            inventory_id=inventory.id,
            user_id=user_id,
            action=InventoryAction.ADJUSTMENT,
            quantity_change=quantity_change,
            previous_quantity=old_quantity,
            new_quantity=inventory.quantity,
            notes=notes
        )
        db.add(log)
        db.commit()
        
        return inventory