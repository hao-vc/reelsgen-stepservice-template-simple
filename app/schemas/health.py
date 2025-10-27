"""Health check schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response schema."""
    
    status: Literal["healthy", "unhealthy"] = Field(
        description="Service health status"
    )
    service_name: str = Field(description="Name of the service")
    version: str = Field(description="Service version")
    uptime: str = Field(description="Service uptime in human readable format")
    timestamp: datetime = Field(description="Current timestamp")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }
