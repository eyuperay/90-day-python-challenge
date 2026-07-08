from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task


class TaskService:
    @staticmethod
    async def list_all(db: AsyncSession):
        result = await db.execute(select(Task))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, task_id: int):
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, **payload):
        task = Task(**payload)
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete(db: AsyncSession, task: Task):
        await db.delete(task)
        await db.commit()