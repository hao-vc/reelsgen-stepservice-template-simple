"""Health check API endpoint."""

import time
from datetime import datetime, timedelta

from fastapi import APIRouter

from app.config import settings
from app.logging_config import get_logger
from app.schemas.health import HealthResponse

logger = get_logger(__name__)
router = APIRouter()

# Store service start time
_start_time = datetime.utcnow()


def format_uptime() -> str:
    """Format uptime in human readable format."""
    uptime = datetime.utcnow() - _start_time
    
    # Convert to total seconds
    total_seconds = int(uptime.total_seconds())
    
    # Calculate components
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    # Format uptime string
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    
    return " ".join(parts)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the service",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    logger.info("Health check requested")
    
    return HealthResponse(
        status="healthy",
        service_name=settings.service_name,
        version=settings.service_version,
        uptime=format_uptime(),
        timestamp=datetime.utcnow(),
    )
