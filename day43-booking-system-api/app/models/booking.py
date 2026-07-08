import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"
    no_show = "no_show"


# State machine: maps current status → set of valid next statuses
BOOKING_STATUS_TRANSITIONS: dict[BookingStatus, set[BookingStatus]] = {
    BookingStatus.pending: {BookingStatus.confirmed, BookingStatus.cancelled},
    BookingStatus.confirmed: {
        BookingStatus.completed,
        BookingStatus.cancelled,
        BookingStatus.no_show,
    },
    # Terminal states — no further transitions allowed
    BookingStatus.completed: set(),
    BookingStatus.cancelled: set(),
    BookingStatus.no_show: set(),
}


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Snapshot of service details at booking time (service may change later)
    service_name_snapshot: Mapped[str] = mapped_column(String(255), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus),
        nullable=False,
        default=BookingStatus.pending,
        index=True,
    )

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    cancelled_by: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )  # "customer" | "provider" | "admin"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    customer: Mapped["User"] = relationship(  # noqa: F821
        "User", back_populates="bookings_as_customer", foreign_keys=[customer_id]
    )
    provider: Mapped["Provider"] = relationship(  # noqa: F821
        "Provider", back_populates="bookings"
    )
    service: Mapped["Service"] = relationship(  # noqa: F821
        "Service", back_populates="bookings"
    )
    review: Mapped["Review"] = relationship(  # noqa: F821
        "Review", back_populates="booking", uselist=False
    )
