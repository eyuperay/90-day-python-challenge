from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.deal import Deal
from app.schemas.deal import DealCreate, DealUpdate

class DealService:
    @staticmethod
    def get_deals(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        stage: Optional[str] = None,
        customer_id: Optional[int] = None
    ):
        query = db.query(Deal)
        if stage:
            query = query.filter(Deal.stage == stage)
        if customer_id:
            query = query.filter(Deal.customer_id == customer_id)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_deal_by_id(db: Session, deal_id: int):
        return db.query(Deal).filter(Deal.id == deal_id).first()
    
    @staticmethod
    def create_deal(db: Session, deal: DealCreate):
        db_deal = Deal(**deal.model_dump())
        db.add(db_deal)
        db.commit()
        db.refresh(db_deal)
        return db_deal
    
    @staticmethod
    def update_deal(db: Session, deal_id: int, deal: DealUpdate):
        db_deal = db.query(Deal).filter(Deal.id == deal_id).first()
        if not db_deal:
            return None
        for key, value in deal.model_dump(exclude_unset=True).items():
            setattr(db_deal, key, value)
        db.commit()
        db.refresh(db_deal)
        return db_deal
    
    @staticmethod
    def delete_deal(db: Session, deal_id: int):
        deal = db.query(Deal).filter(Deal.id == deal_id).first()
        if not deal:
            return False
        db.delete(deal)
        db.commit()
        return True