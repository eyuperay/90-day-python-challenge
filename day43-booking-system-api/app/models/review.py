from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Review(Base):
    """
    A customer review for a completed booking.
    One review per booking (enforced via unique constraint on booking_id).
    Rating: 1–5 stars (enforced via CheckConstraint).
    """

    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_range"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    booking_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("bookings.id", ondelete="CASCADE"),
        unique=True,  # one review per booking
        nullable=False,
        index=True,
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1–5
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    booking: Mapped["Booking"] = relationship("Booking", back_populates="review")  # noqa: F821
    customer: Mapped["User"] = relationship("User", back_populates="reviews")  # noqa: F821
    provider: Mapped["Provider"] = relationship("Provider", back_populates="reviews")  # noqa: F821
