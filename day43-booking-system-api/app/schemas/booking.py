from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.models.booking import BookingStatus


class BookingCreateRequest(BaseModel):
    provider_id: int
    service_id: int
    start_datetime: datetime
    notes: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def start_in_future(self) -> "BookingCreateRequest":
        from datetime import timezone

        if self.start_datetime.tzinfo is None:
            raise ValueError("start_datetime must be timezone-aware (include UTC offset).")
        if self.start_datetime <= datetime.now(timezone.utc):
            raise ValueError("start_datetime must be in the future.")
        return self


class BookingCancelRequest(BaseModel):
    reason: str = Field(..., min_length=5, max_length=500)


class BookingResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    customer_id: int
    provider_id: int
    service_id: int | None
    service_name_snapshot: str
    duration_minutes: int
    price: float
    start_datetime: datetime
    end_datetime: datetime
    status: BookingStatus
    notes: str | None
    cancellation_reason: str | None
    cancelled_by: str | None
    created_at: datetime
    updated_at: datetime


class BookingListFilters(BaseModel):
    status: BookingStatus | None = None
    provider_id: int | None = None
    customer_id: int | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None
