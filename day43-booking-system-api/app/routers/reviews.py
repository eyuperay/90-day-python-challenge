from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.schemas.review import ReviewCreateRequest, ReviewResponse
from app.services import review_service
from app.utils.pagination import PaginationParams

router = APIRouter()


@router.post("/", response_model=ReviewResponse, status_code=201)
async def create_review(
    payload: ReviewCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit a review for a completed booking.
    Only the customer who made the booking can review it. One review per booking.
    """
    return await review_service.create_review(payload, current_user, db)


@router.get("/my", response_model=list[ReviewResponse])
async def my_reviews(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all reviews left by the current user."""
    return await review_service.get_my_reviews(
        current_user.id, db, skip=pagination.offset, limit=pagination.limit
    )


@router.get("/provider/{provider_id}", response_model=list[ReviewResponse])
async def provider_reviews(
    provider_id: int,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Get reviews for a specific provider. Public endpoint."""
    return await review_service.get_provider_reviews(
        provider_id, db, skip=pagination.offset, limit=pagination.limit
    )


@router.delete("/{review_id}", status_code=204)
async def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a review. Customers delete their own; admins can delete any."""
    await review_service.delete_review(review_id, current_user, db)
