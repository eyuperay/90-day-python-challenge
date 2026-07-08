from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, users, services, providers, availability, bookings, reviews


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create all tables (dev / test convenience; prod uses Alembic)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description=(
            "Production-grade appointment booking API. "
            "Supports multi-provider scheduling, real-time slot availability, "
            "booking lifecycle management, and customer reviews."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(services.router, prefix="/services", tags=["Services"])
    app.include_router(providers.router, prefix="/providers", tags=["Providers"])
    app.include_router(availability.router, prefix="/providers", tags=["Availability"])
    app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
    app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok", "app": settings.APP_NAME}

    return app


app = create_app()
