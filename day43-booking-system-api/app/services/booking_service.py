from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.availability import ProviderAvailability, ProviderUnavailability
from app.models.booking import Booking, BookingStatus, BOOKING_STATUS_TRANSITIONS
from app.models.provider import Provider, ProviderService
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.booking import BookingCreateRequest


async def _resolve_service_details(
    provider_id: int, service_id: int, db: AsyncSession
) -> tuple[Service, ProviderService]:
    """Return (Service, ProviderService) or raise 404/422."""
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
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provider does not offer this service.",
        )
    svc_result = await db.execute(select(Service).where(Service.id == service_id))
    service = svc_result.scalar_one_or_none()
    if not service or not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Service not found or inactive.",
        )
    return service, ps


async def _check_conflict(
    provider_id: int,
    start_dt: datetime,
    end_dt: datetime,
    db: AsyncSession,
    exclude_booking_id: int | None = None,
) -> None:
    """Raise 409 if there is an overlapping booking for this provider."""
    q = select(Booking).where(
        Booking.provider_id == provider_id,
        Booking.status.in_([BookingStatus.pending, BookingStatus.confirmed]),
        Booking.start_datetime < end_dt,
        Booking.end_datetime > start_dt,
    )
    if exclude_booking_id is not None:
        q = q.where(Booking.id != exclude_booking_id)
    result = await db.execute(q)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The requested time slot conflicts with an existing booking.",
        )


def _ensure_utc(dt: datetime) -> datetime:
    """Return dt as UTC-aware. Uses replace() only when tzinfo is truly absent."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


async def _validate_within_availability(
    provider_id: int, start_dt: datetime, end_dt: datetime, db: AsyncSession
) -> None:
    """
    Ensure the booking window falls within the provider's weekly availability
    and is not blocked by a ProviderUnavailability record.
    """
    target_date = start_dt.date()

    # 1. Check unavailability blocks (leave, vacation, sick days)
    unavail_result = await db.execute(
        select(ProviderUnavailability).where(
            ProviderUnavailability.provider_id == provider_id,
            ProviderUnavailability.start_date <= target_date,
            ProviderUnavailability.end_date >= target_date,
        )
    )
    if unavail_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provider is not available on the selected date (leave/unavailability block).",
        )

    # 2. Check weekly availability window
    dow = start_dt.weekday()  # 0=Monday, 6=Sunday
    avail_result = await db.execute(
        select(ProviderAvailability).where(
            ProviderAvailability.provider_id == provider_id,
            ProviderAvailability.day_of_week == dow,
            ProviderAvailability.is_active == True,  # noqa: E712
        )
    )
    avail = avail_result.scalar_one_or_none()
    if not avail:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Provider does not have availability on the selected day of the week.",
        )

    # 3. Ensure start/end falls strictly within the availability window
    avail_start = _ensure_utc(
        datetime.combine(target_date, avail.start_time)
    )
    avail_end = _ensure_utc(
        datetime.combine(target_date, avail.end_time)
    )

    if start_dt < avail_start or end_dt > avail_end:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Booking time {start_dt.strftime('%H:%M')}–{end_dt.strftime('%H:%M')} UTC "
                f"falls outside provider's availability window "
                f"{avail.start_time.strftime('%H:%M')}–{avail.end_time.strftime('%H:%M')} UTC."
            ),
        )


async def create_booking(
    payload: BookingCreateRequest, customer: User, db: AsyncSession
) -> Booking:
    # Validate advance booking limit
    now = datetime.now(timezone.utc)
    max_dt = now + timedelta(days=settings.MAX_ADVANCE_BOOKING_DAYS)
    start_dt = _ensure_utc(payload.start_datetime)

    if start_dt > max_dt:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Bookings cannot be made more than {settings.MAX_ADVANCE_BOOKING_DAYS} days in advance.",
        )

    # Validate provider exists and is active
    p_result = await db.execute(
        select(Provider).where(Provider.id == payload.provider_id, Provider.is_active == True)  # noqa: E712
    )
    if not p_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found or inactive."
        )

    service, ps = await _resolve_service_details(payload.provider_id, payload.service_id, db)
    duration = ps.duration_override_minutes or service.duration_minutes
    price = float(ps.price_override if ps.price_override is not None else service.base_price)

    end_dt = start_dt + timedelta(minutes=duration)

    # Validate booking falls within provider's working schedule
    await _validate_within_availability(payload.provider_id, start_dt, end_dt, db)

    # Conflict check against existing bookings
    await _check_conflict(payload.provider_id, start_dt, end_dt, db)

    booking = Booking(
        customer_id=customer.id,
        provider_id=payload.provider_id,
        service_id=payload.service_id,
        service_name_snapshot=service.name,
        duration_minutes=duration,
        price=price,
        start_datetime=start_dt,
        end_datetime=end_dt,
        notes=payload.notes,
        status=BookingStatus.pending,
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    return booking


def _assert_transition(booking: Booking, target: BookingStatus) -> None:
    allowed = BOOKING_STATUS_TRANSITIONS.get(booking.status, set())
    if target not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Cannot transition booking from '{booking.status}' to '{target}'. "
                f"Allowed transitions: {[s.value for s in allowed] or 'none (terminal state)'}."
            ),
        )


async def get_booking_by_id(booking_id: int, db: AsyncSession) -> Booking:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")
    return booking


async def _get_actor_provider(actor: User, db: AsyncSession) -> Provider | None:
    """Return the Provider profile for a provider-role user, or None."""
    result = await db.execute(select(Provider).where(Provider.user_id == actor.id))
    return result.scalar_one_or_none()


async def confirm_booking(booking_id: int, actor: User, db: AsyncSession) -> Booking:
    booking = await get_booking_by_id(booking_id, db)
    _assert_transition(booking, BookingStatus.confirmed)

    if actor.role != UserRole.admin:
        provider = await _get_actor_provider(actor, db)
        if not provider or provider.id != booking.provider_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned provider or an admin can confirm this booking.",
            )

    booking.status = BookingStatus.confirmed
    await db.flush()
    await db.refresh(booking)
    return booking


async def complete_booking(booking_id: int, actor: User, db: AsyncSession) -> Booking:
    booking = await get_booking_by_id(booking_id, db)
    _assert_transition(booking, BookingStatus.completed)

    if actor.role != UserRole.admin:
        provider = await _get_actor_provider(actor, db)
        if not provider or provider.id != booking.provider_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned provider or an admin can complete this booking.",
            )

    booking.status = BookingStatus.completed
    await db.flush()
    await db.refresh(booking)
    return booking


async def cancel_booking(
    booking_id: int, reason: str, actor: User, db: AsyncSession
) -> Booking:
    booking = await get_booking_by_id(booking_id, db)
    _assert_transition(booking, BookingStatus.cancelled)

    if actor.role == UserRole.admin:
        cancelled_by = "admin"
    elif actor.role == UserRole.customer:
        # Customers may only cancel their own bookings
        if booking.customer_id != actor.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own bookings.",
            )
        # Minimum cancellation notice
        now = datetime.now(timezone.utc)
        booking_start = _ensure_utc(booking.start_datetime)
        if booking_start < now + timedelta(hours=settings.MIN_CANCELLATION_HOURS):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"Bookings must be cancelled at least "
                    f"{settings.MIN_CANCELLATION_HOURS} hour(s) in advance."
                ),
            )
        cancelled_by = "customer"
    else:
        # Provider: may only cancel bookings they are assigned to
        provider = await _get_actor_provider(actor, db)
        if not provider or provider.id != booking.provider_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel bookings assigned to you.",
            )
        cancelled_by = "provider"

    booking.status = BookingStatus.cancelled
    booking.cancellation_reason = reason
    booking.cancelled_by = cancelled_by
    await db.flush()
    await db.refresh(booking)
    return booking


async def mark_no_show(booking_id: int, actor: User, db: AsyncSession) -> Booking:
    booking = await get_booking_by_id(booking_id, db)
    _assert_transition(booking, BookingStatus.no_show)

    if actor.role != UserRole.admin:
        provider = await _get_actor_provider(actor, db)
        if not provider or provider.id != booking.provider_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the assigned provider or an admin can mark a no-show.",
            )

    booking.status = BookingStatus.no_show
    await db.flush()
    await db.refresh(booking)
    return booking


async def list_bookings(
    db: AsyncSession,
    customer_id: int | None = None,
    provider_id: int | None = None,
    booking_status: BookingStatus | None = None,
    from_date: datetime | None = None,
    to_date: datetime | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Booking]:
    q = select(Booking)
    if customer_id is not None:
        q = q.where(Booking.customer_id == customer_id)
    if provider_id is not None:
        q = q.where(Booking.provider_id == provider_id)
    if booking_status is not None:
        q = q.where(Booking.status == booking_status)
    if from_date is not None:
        q = q.where(Booking.start_datetime >= from_date)
    if to_date is not None:
        q = q.where(Booking.start_datetime <= to_date)
    q = q.order_by(Booking.start_datetime.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return list(result.scalars().all())
