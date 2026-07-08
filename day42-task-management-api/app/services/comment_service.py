from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.comment import Comment


class CommentService:
    @staticmethod
    async def list_all(db: AsyncSession):
        result = await db.execute(select(Comment))
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, content: str, task_id: int, author_id: int):
        comment = Comment(content=content, task_id=task_id, author_id=author_id)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment