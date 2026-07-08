from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import Inventory


class InventoryService:
    @staticmethod
    async def list_all(db: AsyncSession):
        result = await db.execute(select(Inventory))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, **payload):
        item = Inventory(**payload)
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item