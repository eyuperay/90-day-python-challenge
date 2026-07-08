import json

from app.core.redis_client import redis_client


async def cache_get(key: str):
    value = await redis_client.get(key)
    if value is None:
        return None
    return json.loads(value)


async def cache_set(key: str, value, ttl: int = 300):
    await redis_client.set(key, json.dumps(value), ex=ttl)


async def cache_delete(key: str):
    await redis_client.delete(key)