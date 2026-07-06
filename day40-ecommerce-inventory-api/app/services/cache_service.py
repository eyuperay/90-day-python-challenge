from app.core.redis_client import redis_client
from typing import Optional, Any
import json

class CacheService:
    @staticmethod
    def get_product_cache(key: str) -> Optional[Any]:
        return redis_client.get_cache(key)
    
    @staticmethod
    def set_product_cache(key: str, value: Any, expire: int = 300):
        return redis_client.set_cache(key, value, expire)
    
    @staticmethod
    def clear_product_cache(product_id: Optional[int] = None):
        if product_id:
            redis_client.delete_cache(f"product:{product_id}")
        redis_client.clear_pattern("products:*")
    
    @staticmethod
    def get_products_cache(key: str) -> Optional[Any]:
        return redis_client.get_cache(key)
    
    @staticmethod
    def set_products_cache(key: str, value: Any, expire: int = 300):
        return redis_client.set_cache(key, value, expire)