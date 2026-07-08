# Day43 Booking System API

A production-grade appointment/service booking REST API built with FastAPI, async SQLAlchemy 2.0, and Pydantic v2. Models a real-life service business (salon, clinic, gym, etc.) where customers book time slots with providers.

## Features

- **JWT Authentication** — access + refresh tokens, role-based access (customer / provider / admin)
- **Services Catalog** — services with categories, duration, pricing, and active/inactive toggle
- **Provider Profiles** — users who offer services, with bio, specializations, and per-service pricing overrides
- **Weekly Availability** — providers set recurring availability by day-of-week with time windows
- **Unavailability Blocks** — providers block specific date ranges (holidays, vacation)
- **Smart Time Slots** — available slot generation that avoids conflicts and past times
- **Bookings** — full lifecycle with status state machine
- **Reviews** — customers rate completed bookings (one review per booking)
- **Redis Cache** — provider/service listings and slot responses cached with pattern invalidation
- **Pagination** — cursor-style page/size on all list endpoints
- **Docker + Alembic** — ready for deployment; migrations in `app/alembic/versions/`

## Booking Status State Machine

```
pending ──► confirmed ──► completed
   │              │
   ▼              ▼
cancelled      cancelled
                  │
                  ▼
               no_show
```

- `pending → confirmed` (provider / admin confirms)
- `pending → cancelled` (customer or admin cancels before confirmation)
- `confirmed → completed` (provider / admin marks done)
- `confirmed → cancelled` (customer or provider cancels with reason)
- `confirmed → no_show` (provider marks customer no-show)
- `completed`, `cancelled`, `no_show` are **terminal**

## Project Structure

```
day43-booking-system-api/
├── app/
│   ├── main.py              # FastAPI factory + lifespan
│   ├── core/
│   │   ├── config.py        # pydantic-settings; raises on insecure SECRET_KEY in prod
│   │   ├── database.py      # async engine, session, Base, get_db
│   │   ├── security.py      # JWT create/decode, password hashing
│   │   └── dependencies.py  # get_current_user, role guards
│   ├── models/
│   │   ├── user.py          # User (customer / provider / admin roles)
│   │   ├── service.py       # Service catalog
│   │   ├── provider.py      # Provider profile + ProviderService M2M
│   │   ├── availability.py  # ProviderAvailability + ProviderUnavailability
│   │   ├── booking.py       # Booking + BOOKING_STATUS_TRANSITIONS
│   │   └── review.py        # Review (1-per-booking)
│   ├── schemas/             # Pydantic v2 request/response models
│   ├── routers/             # FastAPI routers (one per domain)
│   ├── services/            # Business logic layer
│   │   ├── booking_service.py    # State machine, conflict detection, slot logic
│   │   ├── availability_service.py # Slot generation algorithm
│   │   └── cache_service.py      # Redis wrapper
│   ├── utils/
│   │   ├── pagination.py    # PaginationParams + Page[T]
│   │   ├── filters.py       # SQLAlchemy filter helpers
│   │   └── time_slots.py    # Time slot math utilities
│   └── alembic/             # Alembic migrations
├── tests/
│   ├── conftest.py          # SQLite in-memory engine, transactional rollback
│   ├── test_auth.py
│   ├── test_services.py
│   ├── test_providers.py
│   ├── test_bookings.py     # State machine + conflict detection tests
│   └── test_reviews.py
├── scripts/
│   ├── seed.py              # Demo data seeder
│   └── deploy.sh
├── .env.example
├── .env.test
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Quick Start

### Local (with Docker)

```bash
cp .env.example .env
docker-compose up --build
```

API docs: http://localhost:8000/docs

### Local (without Docker)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start Postgres and Redis, then:
cp .env.example .env
# Edit .env with your DB/Redis URLs

alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

### Run Tests (no external services needed)

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Key API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register as customer |
| POST | `/auth/login` | Get access + refresh tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/services/` | List all active services |
| POST | `/services/` | Create service (admin) |
| GET | `/providers/` | List all active providers |
| GET | `/providers/{id}/slots` | Get available time slots for a date |
| POST | `/providers/{id}/availability` | Set weekly availability (provider/admin) |
| POST | `/bookings/` | Create a booking |
| GET | `/bookings/my` | My bookings (customer) |
| PATCH | `/bookings/{id}/confirm` | Confirm booking (provider/admin) |
| PATCH | `/bookings/{id}/complete` | Mark completed (provider/admin) |
| PATCH | `/bookings/{id}/cancel` | Cancel with reason |
| PATCH | `/bookings/{id}/no-show` | Mark no-show (provider/admin) |
| POST | `/reviews/` | Leave a review (customer, completed bookings only) |
| GET | `/providers/{id}/reviews` | Provider reviews with avg rating |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT signing key — **change in production** | — |
| `DATABASE_URL` | Async SQLAlchemy URL | postgresql+asyncpg://... |
| `REDIS_URL` | Redis connection string | redis://localhost:6379/0 |
| `MAX_ADVANCE_BOOKING_DAYS` | How far ahead customers can book | 60 |
| `MIN_CANCELLATION_HOURS` | Hours notice required to cancel | 2 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | 7 |
