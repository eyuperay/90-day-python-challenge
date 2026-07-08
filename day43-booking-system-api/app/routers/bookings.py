from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_current_provider_user,
)
from app.models.booking import BookingStatus
from app.models.user import User
from app.schemas.booking import BookingCancelRequest, BookingCreateRequest, BookingResponse
from app.services import booking_service
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=201)
async def create_booking(
    payload: BookingCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new booking. Any authenticated user can book."""
    return await booking_service.create_booking(payload, current_user, db)


@router.get("/my", response_model=list[BookingResponse])
async def my_bookings(
    booking_status: BookingStatus | None = Query(default=None),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the current user's bookings (as a customer)."""
    return await booking_service.list_bookings(
        db,
        customer_id=current_user.id,
        booking_status=booking_status,
        from_date=from_date,
        to_date=to_date,
        skip=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/provider/schedule", response_model=list[BookingResponse])
async def provider_schedule(
    booking_status: BookingStatus | None = Query(default=None),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider] Get all bookings assigned to the current provider."""
    from sqlalchemy import select
    from app.models.provider import Provider

    p_result = await db.execute(select(Provider).where(Provider.user_id == current_user.id))
    provider = p_result.scalar_one_or_none()
    if not provider:
        return []

    return await booking_service.list_bookings(
        db,
        provider_id=provider.id,
        booking_status=booking_status,
        from_date=from_date,
        to_date=to_date,
        skip=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/", response_model=list[BookingResponse])
async def list_all_bookings(
    customer_id: int | None = Query(default=None),
    provider_id: int | None = Query(default=None),
    booking_status: BookingStatus | None = Query(default=None),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),
    pagination: PaginationParams = Depends(),
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] List all bookings with optional filters."""
    return await booking_service.list_bookings(
        db,
        customer_id=customer_id,
        provider_id=provider_id,
        booking_status=booking_status,
        from_date=from_date,
        to_date=to_date,
        skip=pagination.offset,
        limit=pagination.limit,
    )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a single booking. Customers see their own; providers see assigned ones; admins see all."""
    booking = await booking_service.get_booking_by_id(booking_id, db)
    from app.models.user import UserRole
    from sqlalchemy import select
    from app.models.provider import Provider

    if current_user.role == UserRole.admin:
        return booking
    if booking.customer_id == current_user.id:
        return booking
    p_result = await db.execute(select(Provider).where(Provider.user_id == current_user.id))
    provider = p_result.scalar_one_or_none()
    if provider and booking.provider_id == provider.id:
        return booking
    from fastapi import HTTPException, status as http_status
    raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="Access denied.")


@router.patch("/{booking_id}/confirm", response_model=BookingResponse)
async def confirm_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Confirm a pending booking."""
    return await booking_service.confirm_booking(booking_id, current_user, db)


@router.patch("/{booking_id}/complete", response_model=BookingResponse)
async def complete_booking(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Mark a confirmed booking as completed."""
    return await booking_service.complete_booking(booking_id, current_user, db)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    payload: BookingCancelRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Cancel a booking. Customers need MIN_CANCELLATION_HOURS notice."""
    return await booking_service.cancel_booking(booking_id, payload.reason, current_user, db)


@router.patch("/{booking_id}/no-show", response_model=BookingResponse)
async def mark_no_show(
    booking_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Mark a confirmed booking as no-show."""
    return await booking_service.mark_no_show(booking_id, current_user, db)
