from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.user import (
    AdminUserCreateRequest,
    AdminUserUpdateRequest,
    UserResponse,
    UserUpdateRequest,
)
from app.services import user_service
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Get the current user's profile."""
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update name / phone for the current user."""
    return await user_service.update_me(current_user, payload, db)


# ── Admin routes ─────────────────────────────────────────────────────────────

@router.get("/", response_model=list[UserResponse])
async def list_users(
    pagination: PaginationParams = Depends(),
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] List all users."""
    return await user_service.get_all_users(db, skip=pagination.offset, limit=pagination.limit)


@router.post("/", response_model=UserResponse, status_code=201)
async def admin_create_user(
    payload: AdminUserCreateRequest,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Create a user with any role (including provider/admin)."""
    return await user_service.admin_create_user(payload, db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Get a specific user by ID."""
    return await user_service.get_user_by_id(user_id, db)


@router.patch("/{user_id}", response_model=UserResponse)
async def admin_update_user(
    user_id: int,
    payload: AdminUserUpdateRequest,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Update role, status, or details for any user."""
    return await user_service.admin_update_user(user_id, payload, db)
