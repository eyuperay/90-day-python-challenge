from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.availability import ProviderAvailability, ProviderUnavailability
from app.models.booking import Booking, BookingStatus
from app.models.provider import Provider, ProviderService
from app.models.service import Service
from app.schemas.availability import (
    AvailabilityCreateRequest,
    AvailabilityUpdateRequest,
    UnavailabilityCreateRequest,
)
from app.schemas.provider import TimeSlotResponse
from app.utils.time_slots import generate_slots


# ── Weekly availability CRUD ──────────────────────────────────────────────────

async def get_provider_availability(
    provider_id: int, db: AsyncSession
) -> list[ProviderAvailability]:
    result = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.provider_id == provider_id
        )
    )
    return list(result.scalars().all())


async def create_availability(
    provider_id: int, payload: AvailabilityCreateRequest, db: AsyncSession
) -> ProviderAvailability:
    # Provider must exist
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found.")

    # Prevent duplicate day entries (one active window per day)
    dup = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.provider_id == provider_id,
            ProviderAvailability.day_of_week == payload.day_of_week,
            ProviderAvailability.is_active == True,  # noqa: E712
        )
    )
    if dup.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Active availability for day {payload.day_of_week} already exists. "
                   "Update or deactivate it first.",
        )

    avail = ProviderAvailability(
        provider_id=provider_id,
        day_of_week=payload.day_of_week,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )
    db.add(avail)
    await db.flush()
    await db.refresh(avail)
    return avail


async def update_availability(
    provider_id: int,
    avail_id: int,
    payload: AvailabilityUpdateRequest,
    db: AsyncSession,
) -> ProviderAvailability:
    result = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.id == avail_id,
            ProviderAvailability.provider_id == provider_id,
        )
    )
    avail = result.scalar_one_or_none()
    if not avail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Availability record not found."
        )
    if payload.start_time is not None:
        avail.start_time = payload.start_time
    if payload.end_time is not None:
        avail.end_time = payload.end_time
    if payload.is_active is not None:
        avail.is_active = payload.is_active
    await db.flush()
    await db.refresh(avail)
    return avail


async def delete_availability(
    provider_id: int, avail_id: int, db: AsyncSession
) -> None:
    result = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.id == avail_id,
            ProviderAvailability.provider_id == provider_id,
        )
    )
    avail = result.scalar_one_or_none()
    if not avail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Availability record not found."
        )
    await db.delete(avail)


# ── Unavailability CRUD ───────────────────────────────────────────────────────

async def get_provider_unavailabilities(
    provider_id: int, db: AsyncSession
) -> list[ProviderUnavailability]:
    result = await db.execute(
        select(ProviderUnavailability).where(
            ProviderUnavailability.provider_id == provider_id
        )
    )
    return list(result.scalars().all())


async def create_unavailability(
    provider_id: int, payload: UnavailabilityCreateRequest, db: AsyncSession
) -> ProviderUnavailability:
    result = await db.execute(select(Provider).where(Provider.id == provider_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found.")

    unavail = ProviderUnavailability(
        provider_id=provider_id,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
    )
    db.add(unavail)
    await db.flush()
    await db.refresh(unavail)
    return unavail


async def delete_unavailability(
    provider_id: int, unavail_id: int, db: AsyncSession
) -> None:
    result = await db.execute(
        select(ProviderUnavailability).where(
            ProviderUnavailability.id == unavail_id,
            ProviderUnavailability.provider_id == provider_id,
        )
    )
    unavail = result.scalar_one_or_none()
    if not unavail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unavailability record not found."
        )
    await db.delete(unavail)


# ── Available slot generation ─────────────────────────────────────────────────

async def get_available_slots(
    provider_id: int,
    service_id: int,
    target_date: date,
    db: AsyncSession,
) -> list[TimeSlotResponse]:
    """
    Returns available time slots for a given provider+service on a given date.

    Algorithm:
    1. Validate provider and service exist and are active.
    2. Check provider is not blocked (ProviderUnavailability) on that date.
    3. Get the weekly availability window for that day-of-week.
    4. Get existing confirmed/pending bookings for that provider on that date.
    5. Generate slots of `duration_minutes` length, excluding conflicts.
    6. Reject slots in the past.
    7. Reject dates beyond MAX_ADVANCE_BOOKING_DAYS.
    """
    today = date.today()
    max_date = today + timedelta(days=settings.MAX_ADVANCE_BOOKING_DAYS)

    if target_date < today:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cannot query slots in the past.",
        )
    if target_date > max_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Cannot query slots more than {settings.MAX_ADVANCE_BOOKING_DAYS} days in advance.",
        )

    # Validate provider
    p_result = await db.execute(select(Provider).where(Provider.id == provider_id))
    provider = p_result.scalar_one_or_none()
    if not provider or not provider.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found or inactive."
        )

    # Validate provider offers this service (active)
    ps_result = await db.execute(
        select(ProviderService).where(
            ProviderService.provider_id == provider_id,
            ProviderService.service_id == service_id,
            ProviderService.is_active == True,  # noqa: E712
        )
    )
    ps = ps_result.scalar_one_or_none()
    if not ps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider does not offer this service.",
        )

    # Get base service for defaults
    svc_result = await db.execute(select(Service).where(Service.id == service_id))
    service = svc_result.scalar_one_or_none()
    if not service or not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found or inactive."
        )

    effective_duration = ps.duration_override_minutes or service.duration_minutes
    effective_price = float(ps.price_override if ps.price_override is not None else service.base_price)

    # Check unavailability blocks
    unavail_result = await db.execute(
        select(ProviderUnavailability).where(
            ProviderUnavailability.provider_id == provider_id,
            ProviderUnavailability.start_date <= target_date,
            ProviderUnavailability.end_date >= target_date,
        )
    )
    if unavail_result.scalar_one_or_none():
        return []  # Provider is on leave on this date

    # Get weekly availability for this day-of-week (0=Mon, 6=Sun)
    dow = target_date.weekday()  # Python: 0=Monday
    avail_result = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.provider_id == provider_id,
            ProviderAvailability.day_of_week == dow,
            ProviderAvailability.is_active == True,  # noqa: E712
        )
    )
    avail = avail_result.scalar_one_or_none()
    if not avail:
        return []  # Provider does not work on this day

    # Fetch existing bookings for this provider on target_date (non-cancelled).
    # Use full overlap check: any booking that overlaps [day_start, day_end),
    # not just bookings whose start falls within the window.
    day_start = datetime.combine(target_date, avail.start_time).replace(tzinfo=timezone.utc)
    day_end = datetime.combine(target_date, avail.end_time).replace(tzinfo=timezone.utc)

    bookings_result = await db.execute(
        select(Booking).where(
            Booking.provider_id == provider_id,
            Booking.start_datetime < day_end,   # booking starts before window ends
            Booking.end_datetime > day_start,   # booking ends after window starts
            Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
        )
    )
    existing_bookings = list(bookings_result.scalars().all())

    def _to_utc(dt: datetime) -> datetime:
        """Safely convert stored datetime to UTC-aware without reinterpreting existing tz."""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)

    busy_windows = [
        (_to_utc(b.start_datetime), _to_utc(b.end_datetime))
        for b in existing_bookings
    ]

    raw_slots = generate_slots(
        avail_start=datetime.combine(target_date, avail.start_time).replace(tzinfo=timezone.utc),
        avail_end=datetime.combine(target_date, avail.end_time).replace(tzinfo=timezone.utc),
        duration_minutes=effective_duration,
        busy_windows=busy_windows,
    )

    now = datetime.now(timezone.utc)
    return [
        TimeSlotResponse(
            start_datetime=slot_start.isoformat(),
            end_datetime=slot_end.isoformat(),
            provider_id=provider_id,
            service_id=service_id,
            duration_minutes=effective_duration,
            price=effective_price,
        )
        for slot_start, slot_end in raw_slots
        if slot_start > now  # skip past slots
    ]
