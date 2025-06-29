from typing import Any, Optional

class CacheService:
    def __init__(self):
        self.cache = {}
        
    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)
    
    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value
        
    def clear(self) -> None:
        self.cache = {}

# Create a singleton instance
cache_service = CacheService()

# Export both the class and the instance
def get_cache_service() -> CacheService:
    return cache_service

# Explicitly export cache_service for easier access in tests
__all__ = ['CacheService', 'get_cache_service', 'cache_service']