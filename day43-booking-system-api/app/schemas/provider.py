from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserResponse


class ProviderCreateRequest(BaseModel):
    """Admin creates a provider profile for an existing user."""

    user_id: int
    bio: str | None = None
    specializations: str | None = Field(default=None, max_length=500)
    years_of_experience: int | None = Field(default=None, ge=0, le=60)


class ProviderUpdateRequest(BaseModel):
    bio: str | None = None
    specializations: str | None = Field(default=None, max_length=500)
    years_of_experience: int | None = Field(default=None, ge=0, le=60)
    is_active: bool | None = None


class ProviderResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    bio: str | None
    specializations: str | None
    years_of_experience: int | None
    average_rating: float
    total_reviews: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    user: UserResponse


# ── Provider ↔ Service linking ──────────────────────────────────────────────

class ProviderServiceAddRequest(BaseModel):
    service_id: int
    price_override: float | None = Field(default=None, ge=0)
    duration_override_minutes: int | None = Field(default=None, ge=5, le=480)


class ProviderServiceUpdateRequest(BaseModel):
    price_override: float | None = Field(default=None, ge=0)
    duration_override_minutes: int | None = Field(default=None, ge=5, le=480)
    is_active: bool | None = None


class ProviderServiceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    provider_id: int
    service_id: int
    price_override: float | None
    duration_override_minutes: int | None
    is_active: bool
    # Resolved effective values (computed in service layer)
    effective_price: float | None = None
    effective_duration_minutes: int | None = None


# ── Available time slot (computed, not a DB row) ─────────────────────────────

class TimeSlotResponse(BaseModel):
    start_datetime: str  # ISO 8601
    end_datetime: str
    provider_id: int
    service_id: int
    duration_minutes: int
    price: float
