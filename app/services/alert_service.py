"""Alert service for sending error notifications."""

from datetime import datetime
from typing import Any, Dict, Optional

import httpx
from pydantic import BaseModel, Field

from app.config import settings
from app.logging_config import get_logger, log_alert_sent

logger = get_logger(__name__)


class AlertPayload(BaseModel):
    """Alert payload schema."""
    
    text: str = Field(description="Alert description")
    priority: str = Field(description="Alert priority (high, medium, low)")
    timestamp: str = Field(description="Alert timestamp")
    tags: list[str] = Field(description="Alert tags")
    debug_logs: Optional[str] = Field(
        default=None,
        description="Additional debug information"
    )


class AlertService:
    """Service for sending alerts to Supabase Edge Function."""
    
    def __init__(self):
        """Initialize alert service."""
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_alert(
        self,
        text: str,
        priority: str = "high",
        tags: Optional[list[str]] = None,
        debug_logs: Optional[str] = None,
        operation_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Send alert to Supabase Edge Function."""
        
        # Skip if alert webhook is not configured
        if not settings.alert_webhook_url or not settings.alert_api_key:
            logger.warning(
                "Alert webhook not configured, skipping alert",
                alert_text=text,
                priority=priority,
            )
            return
        
        try:
            # Prepare alert payload
            alert_tags = tags or ["incident", "critical", settings.service_name]
            if operation_id:
                alert_tags.append(f"operation:{operation_id}")
            
            payload = AlertPayload(
                text=text,
                priority=priority,
                timestamp=datetime.utcnow().isoformat() + "Z",
                tags=alert_tags,
                debug_logs=debug_logs,
            )
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.alert_api_key}",
            }
            
            # Send alert
            response = await self.client.post(
                str(settings.alert_webhook_url),
                json=payload.model_dump(),
                headers=headers,
            )
            
            # Log alert result
            log_alert_sent(
                logger=logger,
                operation_id=operation_id or "unknown",
                alert_text=text,
                priority=priority,
            )
            
            # Raise exception for non-2xx status codes
            response.raise_for_status()
            
        except httpx.HTTPStatusError as e:
            logger.error(
                "Alert HTTP error",
                alert_text=text,
                status_code=e.response.status_code,
                response_text=e.response.text,
            )
            # Don't raise - alerts should not break the main flow
        except httpx.RequestError as e:
            logger.error(
                "Alert request error",
                alert_text=text,
                error=str(e),
            )
            # Don't raise - alerts should not break the main flow
        except Exception as e:
            logger.error(
                "Unexpected alert error",
                alert_text=text,
                error=str(e),
                exc_info=True,
            )
            # Don't raise - alerts should not break the main flow
    
    async def send_error_alert(
        self,
        error: Exception,
        operation_id: Optional[str] = None,
        endpoint: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Send error alert with context."""
        error_text = f"Error in {settings.service_name}"
        if endpoint:
            error_text += f" at {endpoint}"
        error_text += f": {str(error)}"
        
        debug_logs = f"Error type: {type(error).__name__}"
        if endpoint:
            debug_logs += f"\nEndpoint: {endpoint}"
        if operation_id:
            debug_logs += f"\nOperation ID: {operation_id}"
        
        await self.send_alert(
            text=error_text,
            priority="high",
            tags=["error", "incident", settings.service_name],
            debug_logs=debug_logs,
            operation_id=operation_id,
            **kwargs,
        )
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
