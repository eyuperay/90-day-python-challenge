from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import AdminUserCreateRequest, AdminUserUpdateRequest, UserUpdateRequest


async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 20) -> list[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return list(result.scalars().all())


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


async def update_me(user: User, payload: UserUpdateRequest, db: AsyncSession) -> User:
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.phone is not None:
        user.phone = payload.phone
    await db.flush()
    await db.refresh(user)
    return user


async def admin_create_user(payload: AdminUserCreateRequest, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        phone=payload.phone,
        role=payload.role,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def admin_update_user(
    user_id: int, payload: AdminUserUpdateRequest, db: AsyncSession
) -> User:
    user = await get_user_by_id(user_id, db)
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.phone is not None:
        user.phone = payload.phone
    if payload.role is not None:
        user.role = payload.role
    if payload.is_active is not None:
        user.is_active = payload.is_active
    await db.flush()
    await db.refresh(user)
    return user
