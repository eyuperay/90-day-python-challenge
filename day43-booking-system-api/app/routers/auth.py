from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    PasswordChangeRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new customer account."""
    user = await auth_service.register_user(payload, db)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate and receive access + refresh tokens."""
    return await auth_service.login_user(payload, db)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(payload: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Exchange a refresh token for a new token pair."""
    return await auth_service.refresh_tokens(payload.refresh_token, db)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_active_user)):
    """Return the currently authenticated user's profile."""
    return current_user


@router.post("/change-password", status_code=204)
async def change_password(
    payload: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Change the current user's password."""
    await auth_service.change_password(
        current_user, payload.current_password, payload.new_password, db
    )
