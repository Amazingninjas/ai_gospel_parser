"""
Cache Service
=============
Simple in-memory caching for frequently accessed data.
"""
from typing import Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import json


class CacheService:
    """Simple in-memory cache with TTL support"""

    def __init__(self):
        self._cache: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.utcnow() < expires_at:
                return value
            else:
                # Remove expired entry
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache with TTL (default 5 minutes)"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expires_at)

    def delete(self, key: str):
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        """Clear all cached values"""
        self._cache.clear()

    def cleanup_expired(self):
        """Remove all expired entries"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, (_, expires_at) in self._cache.items()
            if now >= expires_at
        ]
        for key in expired_keys:
            del self._cache[key]


# Global cache instance
cache = CacheService()


def cached(ttl_seconds: int = 300, key_prefix: str = ""):
    """
    Decorator to cache function results.

    Args:
        ttl_seconds: Time to live in seconds (default 5 minutes)
        key_prefix: Optional prefix for cache key
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix or func.__name__]

            # Add args to key
            for arg in args:
                if hasattr(arg, '__dict__'):
                    # Skip complex objects (like database sessions)
                    continue
                key_parts.append(str(arg))

            # Add kwargs to key (sorted for consistency)
            for k, v in sorted(kwargs.items()):
                if hasattr(v, '__dict__'):
                    continue
                key_parts.append(f"{k}={v}")

            # Create hash of key
            key_str = "|".join(key_parts)
            cache_key = hashlib.md5(key_str.encode()).hexdigest()

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)

            return result

        return wrapper
    return decorator
