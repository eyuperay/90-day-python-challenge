import enum
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Enum, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ServiceCategory(str, enum.Enum):
    haircare = "haircare"
    skincare = "skincare"
    massage = "massage"
    fitness = "fitness"
    medical = "medical"
    dental = "dental"
    consulting = "consulting"
    beauty = "beauty"
    wellness = "wellness"
    other = "other"


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[ServiceCategory] = mapped_column(
        Enum(ServiceCategory), nullable=False, default=ServiceCategory.other
    )
    # Default duration in minutes (can be overridden per provider)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    # Default base price (can be overridden per provider)
    base_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)
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
    provider_services: Mapped[list["ProviderService"]] = relationship(  # noqa: F821
        "ProviderService", back_populates="service", cascade="all, delete-orphan"
    )
    bookings: Mapped[list["Booking"]] = relationship(  # noqa: F821
        "Booking", back_populates="service"
    )
