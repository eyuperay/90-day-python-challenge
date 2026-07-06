from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.inventory import Inventory, InventoryLog, InventoryAction
from app.models.product import Product
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse

router = APIRouter()

@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    product_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Inventory)
    
    if product_id:
        query = query.filter(Inventory.product_id == product_id)
    
    inventory_items = query.offset(skip).limit(limit).all()
    
    result = []
    for item in inventory_items:
        item_dict = item.__dict__.copy()
        item_dict['product_name'] = item.product.name if item.product else None
        result.append(InventoryResponse(**item_dict))
    
    return result

@router.get("/{product_id}", response_model=InventoryResponse)
async def get_inventory_by_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Envanter bulunamadı")
    
    inventory_dict = inventory.__dict__.copy()
    inventory_dict['product_name'] = inventory.product.name if inventory.product else None
    return InventoryResponse(**inventory_dict)

@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory(
    inventory_data: InventoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    existing = db.query(Inventory).filter(Inventory.product_id == inventory_data.product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bu ürün için zaten envanter kaydı var")
    
    product = db.query(Product).filter(Product.id == inventory_data.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    
    db_inventory = Inventory(
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity,
        reserved_quantity=inventory_data.reserved_quantity,
        reorder_point=inventory_data.reorder_point,
        available_quantity=inventory_data.quantity - inventory_data.reserved_quantity
    )
    
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    
    inventory_dict = db_inventory.__dict__.copy()
    inventory_dict['product_name'] = db_inventory.product.name if db_inventory.product else None
    return InventoryResponse(**inventory_dict)

@router.put("/{product_id}", response_model=InventoryResponse)
async def update_inventory(
    product_id: int,
    inventory_data: InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    db_inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Envanter bulunamadı")
    
    old_quantity = db_inventory.quantity
    
    for key, value in inventory_data.model_dump(exclude_unset=True).items():
        setattr(db_inventory, key, value)
    
    db_inventory.available_quantity = db_inventory.quantity - db_inventory.reserved_quantity
    db.commit()
    db.refresh(db_inventory)
    
    # Log oluştur
    log = InventoryLog(
        inventory_id=db_inventory.id,
        user_id=current_user.id,
        action=InventoryAction.ADJUSTMENT,
        quantity_change=db_inventory.quantity - old_quantity,
        previous_quantity=old_quantity,
        new_quantity=db_inventory.quantity,
        notes="Manuel güncelleme"
    )
    db.add(log)
    db.commit()
    
    inventory_dict = db_inventory.__dict__.copy()
    inventory_dict['product_name'] = db_inventory.product.name if db_inventory.product else None
    return InventoryResponse(**inventory_dict)