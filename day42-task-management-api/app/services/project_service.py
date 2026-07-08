from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


class ProjectService:
    @staticmethod
    async def list_by_owner(db: AsyncSession, owner_id: int):
        result = await db.execute(select(Project).where(Project.owner_id == owner_id))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, project_id: int, owner_id: int):
        result = await db.execute(
            select(Project).where(Project.id == project_id, Project.owner_id == owner_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, name: str, description: str | None, owner_id: int):
        project = Project(name=name, description=description, owner_id=owner_id)
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def delete(db: AsyncSession, project: Project):
        await db.delete(project)
        await db.commit()