"""
Monitoring & Analytics API Router
==================================
Endpoints for health checks, metrics, and analytics.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.user import User
from models.conversation import Conversation
from services.performance_monitor import monitor
from services.analytics_service import analytics
from routers.auth import get_current_user


router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description="Check if the API is running and healthy"
)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.

    Returns:
        Status information including database connectivity
    """
    # Test database connection
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    }


@router.get(
    "/metrics/performance",
    summary="Performance metrics",
    description="Get API endpoint performance statistics"
)
async def get_performance_metrics():
    """
    Get performance metrics for all API endpoints.

    Returns:
        Performance statistics including response times
    """
    return {
        "endpoints": monitor.get_all_stats(),
        "description": "Response times in milliseconds"
    }


@router.get(
    "/metrics/analytics",
    summary="Usage analytics",
    description="Get usage analytics and statistics"
)
async def get_analytics():
    """
    Get usage analytics.

    Returns:
        Usage statistics and popular content
    """
    return {
        "summary": analytics.get_summary(),
        "popular_verses": analytics.get_popular_verses(10),
        "popular_words": analytics.get_popular_words(10)
    }


@router.get(
    "/metrics/database",
    summary="Database metrics",
    description="Get database usage statistics"
)
async def get_database_metrics(db: Session = Depends(get_db)):
    """
    Get database statistics.

    Returns:
        Database usage metrics
    """
    user_count = db.query(func.count(User.id)).scalar()
    conversation_count = db.query(func.count(Conversation.id)).scalar()

    # Get active users (users with conversations)
    active_users = db.query(func.count(func.distinct(Conversation.user_id))).scalar()

    return {
        "total_users": user_count,
        "active_users": active_users,
        "total_conversations": conversation_count,
        "avg_conversations_per_user": round(conversation_count / max(user_count, 1), 2)
    }


@router.get(
    "/metrics/system",
    summary="System metrics",
    description="Get system health and resource usage"
)
async def get_system_metrics():
    """
    Get system metrics.

    Returns:
        System health information
    """
    import psutil
    import os

    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)

    # Memory usage
    memory = psutil.virtual_memory()
    memory_percent = memory.percent
    memory_used_gb = memory.used / (1024 ** 3)
    memory_total_gb = memory.total / (1024 ** 3)

    # Disk usage
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent
    disk_used_gb = disk.used / (1024 ** 3)
    disk_total_gb = disk.total / (1024 ** 3)

    # Process info
    process = psutil.Process(os.getpid())
    process_memory_mb = process.memory_info().rss / (1024 ** 2)

    return {
        "cpu_percent": round(cpu_percent, 2),
        "memory": {
            "percent": round(memory_percent, 2),
            "used_gb": round(memory_used_gb, 2),
            "total_gb": round(memory_total_gb, 2)
        },
        "disk": {
            "percent": round(disk_percent, 2),
            "used_gb": round(disk_used_gb, 2),
            "total_gb": round(disk_total_gb, 2)
        },
        "process": {
            "memory_mb": round(process_memory_mb, 2),
            "pid": os.getpid()
        }
    }


@router.get(
    "/dashboard",
    summary="Monitoring dashboard",
    description="Get complete monitoring dashboard data"
)
async def monitoring_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete monitoring dashboard data.

    Requires authentication. Combines all metrics into a single response.

    Returns:
        Complete dashboard data
    """
    return {
        "health": (await health_check(db)),
        "performance": (await get_performance_metrics()),
        "analytics": (await get_analytics()),
        "database": (await get_database_metrics(db)),
        "system": (await get_system_metrics())
    }
