"""
Demo data seeder for the Day43 Booking System API.

Creates:
  - 1 admin user
  - 3 provider users + provider profiles
  - 6 services across multiple categories
  - Provider ↔ service links with pricing overrides
  - Weekly availability schedules (Mon–Fri 9–5, Sat 9–1)
  - 5 sample bookings (mix of statuses)
  - 3 reviews

Run with:
    python scripts/seed.py
(from the project root, with .env configured for a real DB)
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, time, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.service import Service, ServiceCategory
from app.models.provider import Provider, ProviderService
from app.models.availability import ProviderAvailability
from app.models.booking import Booking, BookingStatus
from app.models.review import Review
from app.core.database import Base


engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        print("🌱 Seeding database...")

        # ── Users ─────────────────────────────────────────────────────────────
        admin = User(
            email="admin@bookingsystem.com",
            full_name="System Admin",
            hashed_password=get_password_hash("Admin@1234"),
            role=UserRole.admin,
        )
        p1_user = User(
            email="alice@bookingsystem.com",
            full_name="Alice Chen",
            hashed_password=get_password_hash("Provider@1234"),
            role=UserRole.provider,
        )
        p2_user = User(
            email="bob@bookingsystem.com",
            full_name="Bob Martinez",
            hashed_password=get_password_hash("Provider@1234"),
            role=UserRole.provider,
        )
        p3_user = User(
            email="carol@bookingsystem.com",
            full_name="Carol Smith",
            hashed_password=get_password_hash("Provider@1234"),
            role=UserRole.provider,
        )
        cust1 = User(
            email="john@example.com",
            full_name="John Doe",
            hashed_password=get_password_hash("Customer@1234"),
            role=UserRole.customer,
        )
        cust2 = User(
            email="jane@example.com",
            full_name="Jane Park",
            hashed_password=get_password_hash("Customer@1234"),
            role=UserRole.customer,
        )
        db.add_all([admin, p1_user, p2_user, p3_user, cust1, cust2])
        await db.flush()
        print(f"  ✓ Users created ({admin.id}, {p1_user.id}, {p2_user.id}, {p3_user.id})")

        # ── Services ──────────────────────────────────────────────────────────
        svc_deep = Service(
            name="Deep Tissue Massage",
            description="Targets deep layers of muscle and connective tissue.",
            category=ServiceCategory.massage,
            duration_minutes=60,
            base_price=85.0,
        )
        svc_swedish = Service(
            name="Swedish Massage",
            description="Classic relaxation massage with long, gliding strokes.",
            category=ServiceCategory.massage,
            duration_minutes=60,
            base_price=70.0,
        )
        svc_haircut = Service(
            name="Men's Haircut",
            description="Wash, cut, and style.",
            category=ServiceCategory.haircare,
            duration_minutes=45,
            base_price=35.0,
        )
        svc_facial = Service(
            name="Deep Cleansing Facial",
            description="Pore-cleansing facial with steam and extraction.",
            category=ServiceCategory.skincare,
            duration_minutes=75,
            base_price=95.0,
        )
        svc_yoga = Service(
            name="Private Yoga Session",
            description="One-on-one yoga instruction.",
            category=ServiceCategory.fitness,
            duration_minutes=60,
            base_price=80.0,
        )
        svc_consult = Service(
            name="Business Consulting",
            description="Strategy and growth consulting session.",
            category=ServiceCategory.consulting,
            duration_minutes=90,
            base_price=200.0,
        )
        db.add_all([svc_deep, svc_swedish, svc_haircut, svc_facial, svc_yoga, svc_consult])
        await db.flush()
        print(f"  ✓ Services created (6 services)")

        # ── Providers ─────────────────────────────────────────────────────────
        p1 = Provider(
            user_id=p1_user.id,
            bio="Licensed massage therapist with 8 years of experience in therapeutic and relaxation massage.",
            specializations="Deep Tissue, Swedish, Sports, Prenatal",
            years_of_experience=8,
        )
        p2 = Provider(
            user_id=p2_user.id,
            bio="Professional barber and hair stylist. Creating great looks since 2015.",
            specializations="Men's grooming, Beard sculpting, Hair coloring",
            years_of_experience=9,
        )
        p3 = Provider(
            user_id=p3_user.id,
            bio="Certified aesthetician and yoga instructor. Holistic wellness professional.",
            specializations="Facials, Body wraps, Yoga, Meditation",
            years_of_experience=6,
        )
        db.add_all([p1, p2, p3])
        await db.flush()
        print(f"  ✓ Provider profiles created")

        # ── Provider Services ─────────────────────────────────────────────────
        ps_links = [
            ProviderService(provider_id=p1.id, service_id=svc_deep.id, price_override=95.0),
            ProviderService(provider_id=p1.id, service_id=svc_swedish.id),
            ProviderService(provider_id=p2.id, service_id=svc_haircut.id, price_override=40.0, duration_override_minutes=50),
            ProviderService(provider_id=p3.id, service_id=svc_facial.id, price_override=110.0),
            ProviderService(provider_id=p3.id, service_id=svc_yoga.id),
        ]
        db.add_all(ps_links)
        await db.flush()
        print(f"  ✓ Provider-service links created")

        # ── Availability ──────────────────────────────────────────────────────
        for provider in [p1, p2, p3]:
            for dow in range(5):  # Mon–Fri
                db.add(ProviderAvailability(
                    provider_id=provider.id,
                    day_of_week=dow,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                ))
            # Saturday half-day
            db.add(ProviderAvailability(
                provider_id=provider.id,
                day_of_week=5,
                start_time=time(9, 0),
                end_time=time(13, 0),
            ))
        await db.flush()
        print(f"  ✓ Availability windows set (Mon–Sat)")

        # ── Bookings ──────────────────────────────────────────────────────────
        now = datetime.now(timezone.utc)

        def weekday_dt(offset_days: int, hour: int) -> datetime:
            dt = now + timedelta(days=offset_days)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)
            return dt.replace(hour=hour, minute=0, second=0, microsecond=0)

        b1 = Booking(
            customer_id=cust1.id, provider_id=p1.id, service_id=svc_deep.id,
            service_name_snapshot="Deep Tissue Massage", duration_minutes=60, price=95.0,
            start_datetime=weekday_dt(3, 10), end_datetime=weekday_dt(3, 10) + timedelta(hours=1),
            status=BookingStatus.confirmed, notes="First time, please be gentle.",
        )
        b2 = Booking(
            customer_id=cust2.id, provider_id=p1.id, service_id=svc_swedish.id,
            service_name_snapshot="Swedish Massage", duration_minutes=60, price=70.0,
            start_datetime=weekday_dt(5, 14), end_datetime=weekday_dt(5, 14) + timedelta(hours=1),
            status=BookingStatus.pending,
        )
        b3 = Booking(
            customer_id=cust1.id, provider_id=p2.id, service_id=svc_haircut.id,
            service_name_snapshot="Men's Haircut", duration_minutes=50, price=40.0,
            start_datetime=now - timedelta(days=3), end_datetime=now - timedelta(days=3) + timedelta(minutes=50),
            status=BookingStatus.completed,
        )
        b4 = Booking(
            customer_id=cust2.id, provider_id=p3.id, service_id=svc_facial.id,
            service_name_snapshot="Deep Cleansing Facial", duration_minutes=75, price=110.0,
            start_datetime=now - timedelta(days=7), end_datetime=now - timedelta(days=7) + timedelta(minutes=75),
            status=BookingStatus.completed,
        )
        b5 = Booking(
            customer_id=cust1.id, provider_id=p3.id, service_id=svc_yoga.id,
            service_name_snapshot="Private Yoga Session", duration_minutes=60, price=80.0,
            start_datetime=now - timedelta(days=1), end_datetime=now - timedelta(days=1) + timedelta(hours=1),
            status=BookingStatus.no_show,
        )
        db.add_all([b1, b2, b3, b4, b5])
        await db.flush()
        print(f"  ✓ Sample bookings created (5)")

        # ── Reviews ───────────────────────────────────────────────────────────
        r1 = Review(
            booking_id=b3.id, customer_id=cust1.id, provider_id=p2.id,
            rating=5, comment="Bob is amazing! Best haircut I've had in years.",
        )
        r2 = Review(
            booking_id=b4.id, customer_id=cust2.id, provider_id=p3.id,
            rating=4, comment="Excellent facial, my skin feels incredible. Highly recommend.",
        )
        db.add_all([r1, r2])
        await db.flush()

        # Update aggregate ratings
        for provider, review in [(p2, r1), (p3, r2)]:
            provider.average_rating = float(review.rating)
            provider.total_reviews = 1

        await db.commit()
        print(f"  ✓ Reviews created + provider ratings updated")
        print("\n✅ Seeding complete!")
        print("\n📋 Login credentials:")
        print("   Admin:    admin@bookingsystem.com / Admin@1234")
        print("   Provider: alice@bookingsystem.com / Provider@1234")
        print("   Provider: bob@bookingsystem.com   / Provider@1234")
        print("   Provider: carol@bookingsystem.com / Provider@1234")
        print("   Customer: john@example.com        / Customer@1234")
        print("   Customer: jane@example.com        / Customer@1234")


if __name__ == "__main__":
    asyncio.run(seed())
