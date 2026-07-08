from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: EmailStr
    full_name: str
    phone: str | None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = Field(default=None, max_length=20)


class AdminUserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    phone: str | None = None
    role: UserRole = UserRole.customer


class AdminUserUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=255)
    phone: str | None = None
    role: UserRole | None = None
    is_active: bool | None = None
