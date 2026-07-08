from __future__ import annotations

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_DEFAULT = "changeme-use-a-long-random-string-in-production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Day43 Booking System API"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    SECRET_KEY: str = _INSECURE_DEFAULT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "sqlite+aiosqlite:///./booking.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    MAX_ADVANCE_BOOKING_DAYS: int = 60
    MIN_CANCELLATION_HOURS: int = 2

    def __init__(self, **data):
        super().__init__(**data)
        if (
            self.SECRET_KEY == _INSECURE_DEFAULT
            and self.ENVIRONMENT not in ("development", "test")
        ):
            raise ValueError(
                "SECRET_KEY must be changed from the default value in non-development environments. "
                "Set the SECRET_KEY environment variable to a strong random string."
            )


settings = Settings()
