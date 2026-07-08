import json
from typing import Any, Optional

import redis.asyncio as aioredis

from app.core.config import settings

_redis_client: Optional[aioredis.Redis] = None


def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


class CacheService:
    def __init__(self, redis: aioredis.Redis | None = None):
        self._redis = redis or get_redis()

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self._redis.get(key)
            return json.loads(value) if value is not None else None
        except Exception:
            return None

    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        try:
            await self._redis.set(key, json.dumps(value, default=str), ex=ttl)
            return True
        except Exception:
            return False

    async def delete(self, key: str) -> bool:
        try:
            await self._redis.delete(key)
            return True
        except Exception:
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Delete all keys matching a glob-style pattern. Returns count deleted."""
        try:
            keys = await self._redis.keys(pattern)
            if keys:
                return await self._redis.delete(*keys)
            return 0
        except Exception:
            return 0

    async def increment(self, key: str, amount: int = 1, ttl: int = 3600) -> int:
        try:
            value = await self._redis.incrby(key, amount)
            await self._redis.expire(key, ttl)
            return value
        except Exception:
            return 0
