from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate

class LeadService:
    @staticmethod
    def get_leads(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None
    ):
        query = db.query(Lead)
        if search:
            query = query.filter(
                (Lead.first_name.ilike(f"%{search}%")) |
                (Lead.last_name.ilike(f"%{search}%")) |
                (Lead.email.ilike(f"%{search}%")) |
                (Lead.company.ilike(f"%{search}%"))
            )
        if status:
            query = query.filter(Lead.status == status)
        if source:
            query = query.filter(Lead.source == source)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_lead_by_id(db: Session, lead_id: int):
        return db.query(Lead).filter(Lead.id == lead_id).first()
    
    @staticmethod
    def create_lead(db: Session, lead: LeadCreate):
        db_lead = Lead(**lead.model_dump())
        db.add(db_lead)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    
    @staticmethod
    def update_lead(db: Session, lead_id: int, lead: LeadUpdate):
        db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not db_lead:
            return None
        for key, value in lead.model_dump(exclude_unset=True).items():
            setattr(db_lead, key, value)
        db.commit()
        db.refresh(db_lead)
        return db_lead
    
    @staticmethod
    def delete_lead(db: Session, lead_id: int):
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            return False
        db.delete(lead)
        db.commit()
        return True