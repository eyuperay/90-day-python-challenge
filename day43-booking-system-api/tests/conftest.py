"""
Shared test fixtures.

- Uses SQLite in-memory (aiosqlite) — no real Postgres or Redis needed.
- Each test function gets a clean transactional session that rolls back after the test.
- Provides ready-made fixtures for users, tokens, providers, services, and bookings.
"""
import os
import pytest
import pytest_asyncio
from datetime import datetime, timedelta, timezone, time, date

os.environ.setdefault("ENV_FILE", ".env.test")

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.models.user import User, UserRole
from app.models.service import Service, ServiceCategory
from app.models.provider import Provider, ProviderService
from app.models.availability import ProviderAvailability
from app.models.booking import Booking, BookingStatus

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession):
    """Async HTTP client wired to the test DB session."""
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


# ── User fixtures ─────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def customer_user(db: AsyncSession) -> User:
    user = User(
        email="customer@test.com",
        full_name="Test Customer",
        hashed_password=get_password_hash("password123"),
        role=UserRole.customer,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def provider_user(db: AsyncSession) -> User:
    user = User(
        email="provider@test.com",
        full_name="Test Provider",
        hashed_password=get_password_hash("password123"),
        role=UserRole.provider,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def admin_user(db: AsyncSession) -> User:
    user = User(
        email="admin@test.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("password123"),
        role=UserRole.admin,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


# ── Token fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture
def customer_token(customer_user: User) -> str:
    return create_access_token({"sub": str(customer_user.id), "role": customer_user.role})


@pytest.fixture
def provider_token(provider_user: User) -> str:
    return create_access_token({"sub": str(provider_user.id), "role": provider_user.role})


@pytest.fixture
def admin_token(admin_user: User) -> str:
    return create_access_token({"sub": str(admin_user.id), "role": admin_user.role})


# ── Service fixtures ──────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def test_service(db: AsyncSession) -> Service:
    service = Service(
        name="Deep Tissue Massage",
        description="60-minute therapeutic massage",
        category=ServiceCategory.massage,
        duration_minutes=60,
        base_price=80.0,
    )
    db.add(service)
    await db.flush()
    await db.refresh(service)
    return service


# ── Provider fixtures ─────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def test_provider(provider_user: User, db: AsyncSession) -> Provider:
    provider = Provider(
        user_id=provider_user.id,
        bio="Certified massage therapist with 5 years experience.",
        specializations="Deep tissue, Sports, Swedish",
        years_of_experience=5,
    )
    db.add(provider)
    await db.flush()
    await db.refresh(provider)
    return provider


@pytest_asyncio.fixture
async def provider_with_service(
    test_provider: Provider, test_service: Service, db: AsyncSession
) -> tuple[Provider, ProviderService]:
    ps = ProviderService(
        provider_id=test_provider.id,
        service_id=test_service.id,
    )
    db.add(ps)
    await db.flush()
    await db.refresh(ps)
    return test_provider, ps


@pytest_asyncio.fixture
async def provider_with_availability(
    provider_with_service: tuple[Provider, ProviderService], db: AsyncSession
) -> Provider:
    provider, _ = provider_with_service
    # Available Monday–Friday 09:00–17:00
    for dow in range(5):
        avail = ProviderAvailability(
            provider_id=provider.id,
            day_of_week=dow,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        db.add(avail)
    await db.flush()
    return provider


# ── Booking fixtures ──────────────────────────────────────────────────────────

def _next_weekday(n: int = 1) -> datetime:
    """Return a datetime n weekdays from now at 10:00 UTC."""
    dt = datetime.now(timezone.utc).replace(hour=10, minute=0, second=0, microsecond=0)
    dt += timedelta(days=1)
    while dt.weekday() >= 5:  # skip weekends
        dt += timedelta(days=1)
    for _ in range(n - 1):
        dt += timedelta(days=1)
        while dt.weekday() >= 5:
            dt += timedelta(days=1)
    return dt


@pytest_asyncio.fixture
async def pending_booking(
    customer_user: User,
    provider_with_availability: Provider,
    test_service: Service,
    db: AsyncSession,
) -> Booking:
    start = _next_weekday(1)
    booking = Booking(
        customer_id=customer_user.id,
        provider_id=provider_with_availability.id,
        service_id=test_service.id,
        service_name_snapshot=test_service.name,
        duration_minutes=test_service.duration_minutes,
        price=float(test_service.base_price),
        start_datetime=start,
        end_datetime=start + timedelta(minutes=test_service.duration_minutes),
        status=BookingStatus.pending,
    )
    db.add(booking)
    await db.flush()
    await db.refresh(booking)
    return booking


@pytest_asyncio.fixture
async def confirmed_booking(pending_booking: Booking, db: AsyncSession) -> Booking:
    pending_booking.status = BookingStatus.confirmed
    await db.flush()
    await db.refresh(pending_booking)
    return pending_booking
