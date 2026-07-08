from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import Service
from app.schemas.service import ServiceCreateRequest, ServiceUpdateRequest


async def get_all_services(
    db: AsyncSession,
    active_only: bool = True,
    skip: int = 0,
    limit: int = 20,
) -> list[Service]:
    q = select(Service)
    if active_only:
        q = q.where(Service.is_active == True)  # noqa: E712
    q = q.offset(skip).limit(limit)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_service_by_id(service_id: int, db: AsyncSession) -> Service:
    result = await db.execute(select(Service).where(Service.id == service_id))
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found.")
    return service


async def create_service(payload: ServiceCreateRequest, db: AsyncSession) -> Service:
    # Prevent duplicate names
    result = await db.execute(select(Service).where(Service.name == payload.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Service '{payload.name}' already exists.",
        )
    service = Service(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        duration_minutes=payload.duration_minutes,
        base_price=payload.base_price,
    )
    db.add(service)
    await db.flush()
    await db.refresh(service)
    return service


async def update_service(
    service_id: int, payload: ServiceUpdateRequest, db: AsyncSession
) -> Service:
    service = await get_service_by_id(service_id, db)
    if payload.name is not None:
        # Check uniqueness (excluding self)
        result = await db.execute(
            select(Service).where(Service.name == payload.name, Service.id != service_id)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Service name '{payload.name}' is already taken.",
            )
        service.name = payload.name
    if payload.description is not None:
        service.description = payload.description
    if payload.category is not None:
        service.category = payload.category
    if payload.duration_minutes is not None:
        service.duration_minutes = payload.duration_minutes
    if payload.base_price is not None:
        service.base_price = payload.base_price
    if payload.is_active is not None:
        service.is_active = payload.is_active
    await db.flush()
    await db.refresh(service)
    return service


async def delete_service(service_id: int, db: AsyncSession) -> None:
    service = await get_service_by_id(service_id, db)
    await db.delete(service)
