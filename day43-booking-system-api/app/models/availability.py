from datetime import date, datetime, time, timezone

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ProviderAvailability(Base):
    """
    Recurring weekly availability window for a provider.
    day_of_week: 0=Monday … 6=Sunday
    """

    __tablename__ = "provider_availabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)  # 0–6
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
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

    provider: Mapped["Provider"] = relationship(  # noqa: F821
        "Provider", back_populates="availabilities"
    )


class ProviderUnavailability(Base):
    """
    Specific date range during which a provider is NOT available.
    Used for vacations, sick days, special closures.
    """

    __tablename__ = "provider_unavailabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id", ondelete="CASCADE"), nullable=False, index=True
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    provider: Mapped["Provider"] = relationship(  # noqa: F821
        "Provider", back_populates="unavailabilities"
    )
