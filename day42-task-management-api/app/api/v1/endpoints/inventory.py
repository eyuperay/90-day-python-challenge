from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.inventory import Inventory
from app.models.user import User
from app.schemas.inventory import InventoryCreate, InventoryRead

router = APIRouter()


@router.get("/", response_model=list[InventoryRead])
async def list_inventory(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Inventory))
    return result.scalars().all()


@router.post("/", response_model=InventoryRead)
async def create_inventory(
    payload: InventoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = Inventory(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item