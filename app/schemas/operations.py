"""Operation schemas for general operations."""

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class OperationRequest(BaseModel):
    """Base operation request schema."""
    
    webhook_url: HttpUrl = Field(description="URL to send operation result")
    data: Dict[str, Any] = Field(description="Operation data")


class OperationResponse(BaseModel):
    """Operation response schema."""
    
    operation_id: UUID = Field(description="Unique operation identifier")
    status: str = Field(description="Operation status")
    message: str = Field(description="Operation message")


class WebhookPayload(BaseModel):
    """Webhook payload schema."""
    
    operation_id: UUID = Field(description="Unique operation identifier")
    status: str = Field(description="Operation status")
    result: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Operation result data"
    )
    error: Optional[str] = Field(
        default=None, 
        description="Error message if operation failed"
    )
    timestamp: str = Field(description="Operation completion timestamp")
