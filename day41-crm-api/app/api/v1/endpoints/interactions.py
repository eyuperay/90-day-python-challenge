from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionCreate, InteractionResponse

router = APIRouter()

@router.get("/", response_model=List[InteractionResponse])
async def get_interactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[int] = None,
    lead_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Interaction)
    if customer_id:
        query = query.filter(Interaction.customer_id == customer_id)
    if lead_id:
        query = query.filter(Interaction.lead_id == lead_id)
    interactions = query.offset(skip).limit(limit).all()
    result = []
    for interaction in interactions:
        interaction_dict = interaction.__dict__.copy()
        interaction_dict['user_name'] = interaction.user.full_name if interaction.user else None
        interaction_dict['customer_name'] = interaction.customer.first_name + " " + interaction.customer.last_name if interaction.customer else None
        interaction_dict['lead_name'] = interaction.lead.first_name + " " + interaction.lead.last_name if interaction.lead else None
        result.append(InteractionResponse(**interaction_dict))
    return result

@router.post("/", response_model=InteractionResponse, status_code=status.HTTP_201_CREATED)
async def create_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_interaction = Interaction(
        **interaction.model_dump(),
        user_id=current_user.id
    )
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    interaction_dict = db_interaction.__dict__.copy()
    interaction_dict['user_name'] = current_user.full_name
    interaction_dict['customer_name'] = db_interaction.customer.first_name + " " + db_interaction.customer.last_name if db_interaction.customer else None
    interaction_dict['lead_name'] = db_interaction.lead.first_name + " " + db_interaction.lead.last_name if db_interaction.lead else None
    return InteractionResponse(**interaction_dict)

@router.get("/{interaction_id}", response_model=InteractionResponse)
async def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Etkileşim bulunamadı")
    interaction_dict = interaction.__dict__.copy()
    interaction_dict['user_name'] = interaction.user.full_name if interaction.user else None
    interaction_dict['customer_name'] = interaction.customer.first_name + " " + interaction.customer.last_name if interaction.customer else None
    interaction_dict['lead_name'] = interaction.lead.first_name + " " + interaction.lead.last_name if interaction.lead else None
    return InteractionResponse(**interaction_dict)