import redis
from app.core.config import settings
import json
from typing import Optional, Any

class RedisClient:
    def __init__(self):
        self.client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_keepalive=True,
            socket_connect_timeout=5
        )
    
    def set_cache(self, key: str, value: Any, expire: int = 300) -> bool:
        try:
            serialized = json.dumps(value)
            return self.client.setex(key, expire, serialized)
        except Exception:
            return False
    
    def get_cache(self, key: str) -> Optional[Any]:
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception:
            return None
    
    def delete_cache(self, *keys: str) -> int:
        return self.client.delete(*keys)
    
    def clear_pattern(self, pattern: str) -> int:
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0

redis_client = RedisClient()