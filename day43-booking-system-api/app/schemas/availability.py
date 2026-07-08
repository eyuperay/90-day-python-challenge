from datetime import date, datetime, time

from pydantic import BaseModel, Field, model_validator


class AvailabilityCreateRequest(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday … 6=Sunday")
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def end_after_start(self) -> "AvailabilityCreateRequest":
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class AvailabilityUpdateRequest(BaseModel):
    start_time: time | None = None
    end_time: time | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def end_after_start(self) -> "AvailabilityUpdateRequest":
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class AvailabilityResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    provider_id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool
    created_at: datetime
    updated_at: datetime


# ── Unavailability (date blocks) ─────────────────────────────────────────────

class UnavailabilityCreateRequest(BaseModel):
    start_date: date
    end_date: date
    reason: str | None = Field(default=None, max_length=500)

    @model_validator(mode="after")
    def end_after_start(self) -> "UnavailabilityCreateRequest":
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class UnavailabilityResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    provider_id: int
    start_date: date
    end_date: date
    reason: str | None
    created_at: datetime
