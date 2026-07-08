from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import (
    get_current_active_user,
    get_current_admin_user,
    get_current_provider_user,
)
from app.models.user import User
from app.schemas.provider import (
    ProviderCreateRequest,
    ProviderResponse,
    ProviderServiceAddRequest,
    ProviderServiceResponse,
    ProviderServiceUpdateRequest,
    ProviderUpdateRequest,
    TimeSlotResponse,
)
from app.services import availability_service, provider_service
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.get("/", response_model=list[ProviderResponse])
async def list_providers(
    active_only: bool = Query(default=True),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """List all providers. Public endpoint."""
    return await provider_service.get_all_providers(
        db, active_only=active_only, skip=pagination.offset, limit=pagination.limit
    )


@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(provider_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single provider by ID. Public endpoint."""
    return await provider_service.get_provider_by_id(provider_id, db)


@router.post("/", response_model=ProviderResponse, status_code=201)
async def create_provider(
    payload: ProviderCreateRequest,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Create a provider profile for an existing provider-role user."""
    return await provider_service.create_provider(payload, db)


@router.patch("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: int,
    payload: ProviderUpdateRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Update provider profile. Providers may only update their own profile."""
    return await provider_service.update_provider(provider_id, payload, current_user, db)


# ── Provider Services ─────────────────────────────────────────────────────────

@router.get("/{provider_id}/services", response_model=list[ProviderServiceResponse])
async def list_provider_services(
    provider_id: int,
    db: AsyncSession = Depends(get_db),
):
    """List services offered by a provider. Public endpoint."""
    pss = await provider_service.get_provider_services(provider_id, db)
    # Attach effective values
    results = []
    for ps in pss:
        item = ProviderServiceResponse.model_validate(ps)
        item.effective_price = float(
            ps.price_override if ps.price_override is not None else ps.service.base_price
        )
        item.effective_duration_minutes = (
            ps.duration_override_minutes or ps.service.duration_minutes
        )
        results.append(item)
    return results


@router.post("/{provider_id}/services", response_model=ProviderServiceResponse, status_code=201)
async def add_provider_service(
    provider_id: int,
    payload: ProviderServiceAddRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Add a service to a provider's offerings. Providers may only modify their own."""
    return await provider_service.add_provider_service(provider_id, payload, current_user, db)


@router.patch("/{provider_id}/services/{ps_id}", response_model=ProviderServiceResponse)
async def update_provider_service(
    provider_id: int,
    ps_id: int,
    payload: ProviderServiceUpdateRequest,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Update price/duration override. Providers may only modify their own."""
    return await provider_service.update_provider_service(provider_id, ps_id, payload, current_user, db)


@router.delete("/{provider_id}/services/{ps_id}", status_code=204)
async def remove_provider_service(
    provider_id: int,
    ps_id: int,
    current_user: User = Depends(get_current_provider_user),
    db: AsyncSession = Depends(get_db),
):
    """[Provider/Admin] Remove a service from a provider's offerings. Providers may only modify their own."""
    await provider_service.remove_provider_service(provider_id, ps_id, current_user, db)


# ── Available Slots ───────────────────────────────────────────────────────────

@router.get("/{provider_id}/slots", response_model=list[TimeSlotResponse])
async def get_available_slots(
    provider_id: int,
    service_id: int = Query(..., description="Service ID to book"),
    target_date: date = Query(..., description="Date to query (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get available time slots for a provider+service on a specific date.
    Public endpoint — no auth required.
    """
    return await availability_service.get_available_slots(
        provider_id=provider_id,
        service_id=service_id,
        target_date=target_date,
        db=db,
    )
