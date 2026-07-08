from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Provider(Base):
    """
    A provider is a User with role=provider who can offer services.
    Linked 1-to-1 with User.
    """

    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    specializations: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )  # comma-separated or short text
    years_of_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Aggregate rating (updated on each review)
    average_rating: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_reviews: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
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
    user: Mapped["User"] = relationship("User", back_populates="provider_profile")  # noqa: F821
    provider_services: Mapped[list["ProviderService"]] = relationship(
        "ProviderService", back_populates="provider", cascade="all, delete-orphan"
    )
    availabilities: Mapped[list["ProviderAvailability"]] = relationship(  # noqa: F821
        "ProviderAvailability", back_populates="provider", cascade="all, delete-orphan"
    )
    unavailabilities: Mapped[list["ProviderUnavailability"]] = relationship(  # noqa: F821
        "ProviderUnavailability", back_populates="provider", cascade="all, delete-orphan"
    )
    bookings: Mapped[list["Booking"]] = relationship(  # noqa: F821
        "Booking", back_populates="provider"
    )
    reviews: Mapped[list["Review"]] = relationship(  # noqa: F821
        "Review", back_populates="provider"
    )


class ProviderService(Base):
    """
    M2M join table linking Provider to Service.
    Allows per-provider price and duration overrides.
    """

    __tablename__ = "provider_services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # None means use the Service default
    price_override: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    duration_override_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    provider: Mapped["Provider"] = relationship("Provider", back_populates="provider_services")
    service: Mapped["Service"] = relationship("Service", back_populates="provider_services")  # noqa: F821
