"""Operation service for handling business logic."""

import asyncio
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from app.logging_config import get_logger
from app.schemas.operations import WebhookPayload
from app.services.webhook_service import WebhookService

logger = get_logger(__name__)


class OperationService:
    """Service for handling operations."""
    
    def __init__(self, webhook_service: WebhookService):
        """Initialize operation service."""
        self.webhook_service = webhook_service
    
    async def process_operation(
        self,
        operation_id: UUID,
        data: Dict[str, Any],
        webhook_url: str,
        **kwargs: Any,
    ) -> None:
        """Process an operation asynchronously."""
        try:
            logger.info(
                "Processing operation",
                operation_id=str(operation_id),
                data_keys=list(data.keys()),
                **kwargs,
            )
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
            
            # Process the data (example: simple echo with timestamp)
            result = {
                "processed_data": data,
                "processed_at": datetime.utcnow().isoformat() + "Z",
                "operation_id": str(operation_id),
            }
            
            # Send result via webhook
            await self.webhook_service.send_webhook(
                webhook_url=webhook_url,
                payload=WebhookPayload(
                    operation_id=operation_id,
                    status="completed",
                    result=result,
                    timestamp=datetime.utcnow().isoformat() + "Z",
                ),
            )
            
            logger.info(
                "Operation completed successfully",
                operation_id=str(operation_id),
            )
            
        except Exception as e:
            logger.error(
                "Operation failed",
                operation_id=str(operation_id),
                error=str(e),
                exc_info=True,
            )
            
            # Send error via webhook
            try:
                await self.webhook_service.send_webhook(
                    webhook_url=webhook_url,
                    payload=WebhookPayload(
                        operation_id=operation_id,
                        status="failed",
                        error=str(e),
                        timestamp=datetime.utcnow().isoformat() + "Z",
                    ),
                )
            except Exception as webhook_error:
                logger.error(
                    "Failed to send error webhook",
                    operation_id=str(operation_id),
                    webhook_error=str(webhook_error),
                )
    
    def generate_operation_id(self) -> UUID:
        """Generate a new operation ID."""
        return uuid4()
