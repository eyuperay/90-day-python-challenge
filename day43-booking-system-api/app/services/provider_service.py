from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.provider import Provider, ProviderService
from app.models.service import Service
from app.models.user import User, UserRole
from app.schemas.provider import (
    ProviderCreateRequest,
    ProviderServiceAddRequest,
    ProviderServiceUpdateRequest,
    ProviderUpdateRequest,
)


# ── Ownership guard ───────────────────────────────────────────────────────────

async def assert_provider_owner_or_admin(
    provider_id: int, actor: User, db: AsyncSession
) -> Provider:
    """
    Raise 403 unless the actor is:
    - An admin, OR
    - The provider user whose profile corresponds to `provider_id`.

    Returns the Provider record on success.
    """
    if actor.role == UserRole.admin:
        result = await db.execute(select(Provider).where(Provider.id == provider_id))
        provider = result.scalar_one_or_none()
        if not provider:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found.")
        return provider

    # Non-admin: verify the actor owns this provider profile
    result = await db.execute(
        select(Provider).where(
            Provider.id == provider_id,
            Provider.user_id == actor.id,
        )
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to modify this provider's data.",
        )
    return provider


# ── Provider CRUD ─────────────────────────────────────────────────────────────

async def get_all_providers(
    db: AsyncSession,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 20,
) -> list[Provider]:
    q = (
        select(Provider)
        .options(selectinload(Provider.user))
        .offset(skip)
        .limit(limit)
    )
    if active_only:
        q = q.where(Provider.is_active == True)  # noqa: E712
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_provider_by_id(provider_id: int, db: AsyncSession) -> Provider:
    result = await db.execute(
        select(Provider)
        .options(selectinload(Provider.user))
        .where(Provider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Provider not found."
        )
    return provider


async def create_provider(payload: ProviderCreateRequest, db: AsyncSession) -> Provider:
    # Validate user exists and has provider/admin role
    result = await db.execute(select(User).where(User.id == payload.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    if user.role not in (UserRole.provider, UserRole.admin):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User must have role 'provider' or 'admin' to have a provider profile.",
        )
    # Check no existing profile
    existing = await db.execute(select(Provider).where(Provider.user_id == payload.user_id))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Provider profile already exists for this user.",
        )
    provider = Provider(
        user_id=payload.user_id,
        bio=payload.bio,
        specializations=payload.specializations,
        years_of_experience=payload.years_of_experience,
    )
    db.add(provider)
    await db.flush()
    await db.refresh(provider)
    return await get_provider_by_id(provider.id, db)


async def update_provider(
    provider_id: int, payload: ProviderUpdateRequest, actor: User, db: AsyncSession
) -> Provider:
    await assert_provider_owner_or_admin(provider_id, actor, db)
    provider = await get_provider_by_id(provider_id, db)
    if payload.bio is not None:
        provider.bio = payload.bio
    if payload.specializations is not None:
        provider.specializations = payload.specializations
    if payload.years_of_experience is not None:
        provider.years_of_experience = payload.years_of_experience
    if payload.is_active is not None:
        provider.is_active = payload.is_active
    await db.flush()
    return await get_provider_by_id(provider_id, db)


# ── Provider ↔ Service management ────────────────────────────────────────────

async def add_provider_service(
    provider_id: int, payload: ProviderServiceAddRequest, actor: User, db: AsyncSession
) -> ProviderService:
    await assert_provider_owner_or_admin(provider_id, actor, db)

    # Validate service exists
    svc_result = await db.execute(select(Service).where(Service.id == payload.service_id))
    if not svc_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found.")

    # Check no duplicate
    dup = await db.execute(
        select(ProviderService).where(
            ProviderService.provider_id == provider_id,
            ProviderService.service_id == payload.service_id,
        )
    )
    if dup.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service already added to this provider.",
        )

    ps = ProviderService(
        provider_id=provider_id,
        service_id=payload.service_id,
        price_override=payload.price_override,
        duration_override_minutes=payload.duration_override_minutes,
    )
    db.add(ps)
    await db.flush()
    await db.refresh(ps)
    return ps


async def update_provider_service(
    provider_id: int,
    ps_id: int,
    payload: ProviderServiceUpdateRequest,
    actor: User,
    db: AsyncSession,
) -> ProviderService:
    await assert_provider_owner_or_admin(provider_id, actor, db)

    result = await db.execute(
        select(ProviderService).where(
            ProviderService.id == ps_id,
            ProviderService.provider_id == provider_id,
        )
    )
    ps = result.scalar_one_or_none()
    if not ps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider service link not found.",
        )
    if payload.price_override is not None:
        ps.price_override = payload.price_override
    if payload.duration_override_minutes is not None:
        ps.duration_override_minutes = payload.duration_override_minutes
    if payload.is_active is not None:
        ps.is_active = payload.is_active
    await db.flush()
    await db.refresh(ps)
    return ps


async def remove_provider_service(
    provider_id: int, ps_id: int, actor: User, db: AsyncSession
) -> None:
    await assert_provider_owner_or_admin(provider_id, actor, db)

    result = await db.execute(
        select(ProviderService).where(
            ProviderService.id == ps_id,
            ProviderService.provider_id == provider_id,
        )
    )
    ps = result.scalar_one_or_none()
    if not ps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provider service link not found.",
        )
    await db.delete(ps)


async def get_provider_services(
    provider_id: int, db: AsyncSession
) -> list[ProviderService]:
    result = await db.execute(
        select(ProviderService)
        .options(selectinload(ProviderService.service))
        .where(ProviderService.provider_id == provider_id)
    )
    return list(result.scalars().all())
