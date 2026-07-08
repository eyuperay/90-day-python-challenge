from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.models.provider import Provider
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreateRequest


async def create_review(
    payload: ReviewCreateRequest, customer: User, db: AsyncSession
) -> Review:
    # Booking must exist and belong to this customer
    b_result = await db.execute(select(Booking).where(Booking.id == payload.booking_id))
    booking = b_result.scalar_one_or_none()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found.")
    if booking.customer_id != customer.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only review your own bookings.",
        )
    if booking.status != BookingStatus.completed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Reviews can only be submitted for completed bookings.",
        )
    # One review per booking (unique constraint on booking_id handles DB-level)
    existing = await db.execute(
        select(Review).where(Review.booking_id == payload.booking_id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A review already exists for this booking.",
        )

    review = Review(
        booking_id=payload.booking_id,
        customer_id=customer.id,
        provider_id=booking.provider_id,
        rating=payload.rating,
        comment=payload.comment,
    )
    db.add(review)
    await db.flush()

    # Update provider aggregate rating
    avg_result = await db.execute(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.provider_id == booking.provider_id
        )
    )
    avg_rating, total = avg_result.one()

    p_result = await db.execute(
        select(Provider).where(Provider.id == booking.provider_id)
    )
    provider = p_result.scalar_one_or_none()
    if provider:
        provider.average_rating = float(avg_rating or 0)
        provider.total_reviews = total or 0

    await db.flush()
    await db.refresh(review)
    return review


async def get_provider_reviews(
    provider_id: int, db: AsyncSession, skip: int = 0, limit: int = 20
) -> list[Review]:
    result = await db.execute(
        select(Review)
        .where(Review.provider_id == provider_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_my_reviews(
    customer_id: int, db: AsyncSession, skip: int = 0, limit: int = 20
) -> list[Review]:
    result = await db.execute(
        select(Review)
        .where(Review.customer_id == customer_id)
        .order_by(Review.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(result.scalars().all())


async def delete_review(review_id: int, actor: User, db: AsyncSession) -> None:
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
    from app.models.user import UserRole
    if review.customer_id != actor.id and actor.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews.",
        )
    await db.delete(review)
    await db.flush()  # flush the delete before recomputing aggregate to avoid stale count
    # Recalculate provider rating
    avg_result = await db.execute(
        select(func.avg(Review.rating), func.count(Review.id)).where(
            Review.provider_id == review.provider_id
        )
    )
    avg_rating, total = avg_result.one()
    p_result = await db.execute(select(Provider).where(Provider.id == review.provider_id))
    provider = p_result.scalar_one_or_none()
    if provider:
        provider.average_rating = float(avg_rating or 0)
        provider.total_reviews = total or 0
