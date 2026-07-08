from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.service import ServiceCreateRequest, ServiceResponse, ServiceUpdateRequest
from app.services import service_service
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    active_only: bool = Query(default=True),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """List all services. Public endpoint."""
    return await service_service.get_all_services(
        db, active_only=active_only, skip=pagination.offset, limit=pagination.limit
    )


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single service by ID. Public endpoint."""
    return await service_service.get_service_by_id(service_id, db)


@router.post("/", response_model=ServiceResponse, status_code=201)
async def create_service(
    payload: ServiceCreateRequest,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Create a new service."""
    return await service_service.create_service(payload, db)


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    payload: ServiceUpdateRequest,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Update a service."""
    return await service_service.update_service(service_id, payload, db)


@router.delete("/{service_id}", status_code=204)
async def delete_service(
    service_id: int,
    _admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """[Admin] Hard-delete a service."""
    await service_service.delete_service(service_id, db)
