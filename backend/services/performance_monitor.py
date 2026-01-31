"""
Performance Monitoring Service
===============================
Middleware for monitoring API performance.
"""
from fastapi import Request
import time
import logging

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor API endpoint performance"""

    def __init__(self):
        self.metrics: dict[str, list[float]] = {}

    def record(self, endpoint: str, duration: float):
        """Record endpoint execution time"""
        if endpoint not in self.metrics:
            self.metrics[endpoint] = []

        self.metrics[endpoint].append(duration)

        # Keep only last 100 requests per endpoint
        if len(self.metrics[endpoint]) > 100:
            self.metrics[endpoint] = self.metrics[endpoint][-100:]

    def get_stats(self, endpoint: str) -> dict:
        """Get performance statistics for an endpoint"""
        if endpoint not in self.metrics or not self.metrics[endpoint]:
            return {
                "count": 0,
                "avg_ms": 0,
                "min_ms": 0,
                "max_ms": 0
            }

        durations = self.metrics[endpoint]
        return {
            "count": len(durations),
            "avg_ms": sum(durations) / len(durations),
            "min_ms": min(durations),
            "max_ms": max(durations)
        }

    def get_all_stats(self) -> dict:
        """Get performance statistics for all endpoints"""
        return {
            endpoint: self.get_stats(endpoint)
            for endpoint in self.metrics.keys()
        }


# Global monitor instance
monitor = PerformanceMonitor()


async def performance_middleware(request: Request, call_next):
    """Middleware to measure endpoint performance"""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000

    # Record metric
    endpoint = f"{request.method} {request.url.path}"
    monitor.record(endpoint, duration_ms)

    # Log slow requests (> 1 second)
    if duration_ms > 1000:
        logger.warning(f"Slow request: {endpoint} took {duration_ms:.2f}ms")

    # Add performance header
    response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"

    return response
