from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_provider_user
from app.models.user import User
from app.schemas.availability import (
    AvailabilityCreateRequest,
    AvailabilityResponse,
    AvailabilityUpdateRequest,
    UnavailabilityCreateRequest,
    UnavailabilityResponse,
)
from app.services import availability_service

router = APIRouter()


# ── Weekly Availability ───────────────────────────────────────────────────────

@router.get("/{provider_id}/availability", response_model=list[AvailabilityResponse])
async def get_availability(
    provider_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a provider's weekly availability schedule. Public endpoint."""
    return await availability_service.get_provider_availability(provider_id, db)


@router.post(
    "/{provider_id}/availability",
    response_model=AvailabilityResponse,
    status_code=201,
)
async def create_availability(
    provider_id: int,
    payload: AvailabilityCreateRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Add a weekly availability window. Providers may only set their own."""
    from app.services.provider_service import assert_provider_owner_or_admin
    await assert_provider_owner_or_admin(provider_id, current_user, db)
    return await availability_service.create_availability(provider_id, payload, db)


@router.patch(
    "/{provider_id}/availability/{avail_id}",
    response_model=AvailabilityResponse,
)
async def update_availability(
    provider_id: int,
    avail_id: int,
    payload: AvailabilityUpdateRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Update an availability window. Providers may only update their own."""
    from app.services.provider_service import assert_provider_owner_or_admin
    await assert_provider_owner_or_admin(provider_id, current_user, db)
    return await availability_service.update_availability(provider_id, avail_id, payload, db)


@router.delete("/{provider_id}/availability/{avail_id}", status_code=204)
async def delete_availability(
    provider_id: int,
    avail_id: int,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Remove a weekly availability window. Providers may only remove their own."""
    from app.services.provider_service import assert_provider_owner_or_admin
    await assert_provider_owner_or_admin(provider_id, current_user, db)
    await availability_service.delete_availability(provider_id, avail_id, db)


# ── Unavailability (date blocks) ──────────────────────────────────────────────

@router.get(
    "/{provider_id}/unavailability",
    response_model=list[UnavailabilityResponse],
)
async def get_unavailabilities(
    provider_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a provider's blocked date ranges. Public endpoint."""
    return await availability_service.get_provider_unavailabilities(provider_id, db)


@router.post(
    "/{provider_id}/unavailability",
    response_model=UnavailabilityResponse,
    status_code=201,
)
async def create_unavailability(
    provider_id: int,
    payload: UnavailabilityCreateRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Block a date range. Providers may only set their own."""
    from app.services.provider_service import assert_provider_owner_or_admin
    await assert_provider_owner_or_admin(provider_id, current_user, db)
    return await availability_service.create_unavailability(provider_id, payload, db)


@router.delete("/{provider_id}/unavailability/{unavail_id}", status_code=204)
async def delete_unavailability(
    provider_id: int,
    unavail_id: int,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Remove a blocked date range. Providers may only remove their own."""
    from app.services.provider_service import assert_provider_owner_or_admin
    await assert_provider_owner_or_admin(provider_id, current_user, db)
    await availability_service.delete_unavailability(provider_id, unavail_id, db)
