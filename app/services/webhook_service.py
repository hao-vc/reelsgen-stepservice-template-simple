"""Webhook service for sending HTTP requests."""

from typing import Any, Dict

import httpx
from pydantic import BaseModel

from app.config import settings
from app.logging_config import get_logger, log_webhook_sent

logger = get_logger(__name__)


class WebhookService:
    """Service for sending webhook requests."""
    
    def __init__(self):
        """Initialize webhook service."""
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def send_webhook(
        self,
        webhook_url: str,
        payload: BaseModel,
        **kwargs: Any,
    ) -> None:
        """Send webhook with webhook authentication."""
        try:
            # Prepare headers with webhook authentication
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.webhook_auth_token}",
            }
            
            # Add any additional headers from kwargs
            if "headers" in kwargs:
                headers.update(kwargs["headers"])
            
            # Send webhook
            response = await self.client.post(
                webhook_url,
                json=payload.model_dump(),
                headers=headers,
            )
            
            # Log webhook result
            log_webhook_sent(
                logger=logger,
                operation_id=getattr(payload, "operation_id", "unknown"),
                webhook_url=webhook_url,
                status_code=response.status_code,
            )
            
            # Raise exception for non-2xx status codes
            response.raise_for_status()
            
        except httpx.HTTPStatusError as e:
            logger.error(
                "Webhook HTTP error",
                webhook_url=webhook_url,
                status_code=e.response.status_code,
                response_text=e.response.text,
            )
            raise
        except httpx.RequestError as e:
            logger.error(
                "Webhook request error",
                webhook_url=webhook_url,
                error=str(e),
            )
            raise
        except Exception as e:
            logger.error(
                "Unexpected webhook error",
                webhook_url=webhook_url,
                error=str(e),
                exc_info=True,
            )
            raise
    
    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()
