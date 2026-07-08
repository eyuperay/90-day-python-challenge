from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreateRequest(BaseModel):
    booking_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = Field(default=None, max_length=2000)


class ReviewResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    booking_id: int
    customer_id: int
    provider_id: int
    rating: int
    comment: str | None
    created_at: datetime


class ProviderRatingSummary(BaseModel):
    provider_id: int
    average_rating: float
    total_reviews: int
    reviews: list[ReviewResponse]
