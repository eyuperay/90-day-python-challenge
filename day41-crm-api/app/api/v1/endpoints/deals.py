from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.deal import Deal
from app.models.customer import Customer
from app.schemas.deal import DealCreate, DealUpdate, DealResponse

router = APIRouter()

@router.get("/", response_model=List[DealResponse])
async def get_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    stage: Optional[str] = None,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Deal)
    
    if stage:
        query = query.filter(Deal.stage == stage)
    if customer_id:
        query = query.filter(Deal.customer_id == customer_id)
    
    deals = query.offset(skip).limit(limit).all()
    
    result = []
    for deal in deals:
        deal_dict = deal.__dict__.copy()
        deal_dict['customer_name'] = deal.customer.first_name + " " + deal.customer.last_name if deal.customer else None
        deal_dict['assigned_to_name'] = deal.assigned_to.full_name if deal.assigned_to else None
        result.append(DealResponse(**deal_dict))
    
    return result

@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Anlaşma bulunamadı")
    
    deal_dict = deal.__dict__.copy()
    deal_dict['customer_name'] = deal.customer.first_name + " " + deal.customer.last_name if deal.customer else None
    deal_dict['assigned_to_name'] = deal.assigned_to.full_name if deal.assigned_to else None
    return DealResponse(**deal_dict)

@router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(
    deal: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SALES]))
):
    customer = db.query(Customer).filter(Customer.id == deal.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    db_deal = Deal(**deal.model_dump())
    db.add(db_deal)
    db.commit()
    db.refresh(db_deal)
    
    deal_dict = db_deal.__dict__.copy()
    deal_dict['customer_name'] = customer.first_name + " " + customer.last_name
    deal_dict['assigned_to_name'] = db_deal.assigned_to.full_name if db_deal.assigned_to else None
    return DealResponse(**deal_dict)

@router.put("/{deal_id}", response_model=DealResponse)
async def update_deal(
    deal_id: int,
    deal: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.SALES]))
):
    db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not db_deal:
        raise HTTPException(status_code=404, detail="Anlaşma bulunamadı")
    
    for key, value in deal.model_dump(exclude_unset=True).items():
        setattr(db_deal, key, value)
    
    db.commit()
    db.refresh(db_deal)
    
    deal_dict = db_deal.__dict__.copy()
    deal_dict['customer_name'] = db_deal.customer.first_name + " " + db_deal.customer.last_name if db_deal.customer else None
    deal_dict['assigned_to_name'] = db_deal.assigned_to.full_name if db_deal.assigned_to else None
    return DealResponse(**deal_dict)

@router.delete("/{deal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN]))
):
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Anlaşma bulunamadı")
    
    db.delete(deal)
    db.commit()