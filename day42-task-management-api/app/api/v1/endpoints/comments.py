from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter()


@router.get("/", response_model=list[CommentRead])
async def list_comments(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Comment))
    return result.scalars().all()


@router.post("/", response_model=CommentRead)
async def create_comment(
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = Comment(content=payload.content, task_id=payload.task_id, author_id=current_user.id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment