from datetime import datetime

from pydantic import BaseModel, Field

from app.models.service import ServiceCategory


class ServiceCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: str | None = None
    category: ServiceCategory = ServiceCategory.other
    duration_minutes: int = Field(default=60, ge=5, le=480)
    base_price: float = Field(default=0.0, ge=0)


class ServiceUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    category: ServiceCategory | None = None
    duration_minutes: int | None = Field(default=None, ge=5, le=480)
    base_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ServiceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    description: str | None
    category: ServiceCategory
    duration_minutes: int
    base_price: float
    is_active: bool
    created_at: datetime
    updated_at: datetime
