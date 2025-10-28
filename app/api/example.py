"""Example API endpoint demonstrating simple text processing."""

from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Response, status
from pydantic import BaseModel, Field

from app.logging_config import get_logger, log_request, log_operation_start
from app.schemas.step_schemas import (
    StepCall,
    StepResult,
    FinalStepResult,
    StepResultStep,
    StepResultOutput,
    OperationId,
)
from app.services.alert_service import AlertService
from app.services.webhook_service import WebhookService

logger = get_logger(__name__)
router = APIRouter()

# Initialize services
webhook_service = WebhookService()
alert_service = AlertService()


class TextProcessingService:
    """Service for text processing operations."""
    
    def __init__(self, webhook_service: WebhookService):
        """Initialize text processing service."""
        self.webhook_service = webhook_service
    
    async def process_text(
        self,
        step_id: UUID,
        operation_id: UUID,
        webhook_url: str,
        input_data: Dict[str, Any],
        variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Process text with maximum flexibility."""
        try:
            logger.info(
                "Processing text",
                step_id=str(step_id),
                operation_id=str(operation_id),
                input_keys=list(input_data.keys()),
            )
            
            # Extract text (required)
            text = input_data.get("text", "")
            if not text:
                raise ValueError("Text is required")
            
            # Extract optional parameters with defaults
            operation = input_data.get("operation", "uppercase")
            language = input_data.get("language", "en")
            format_type = input_data.get("format", "plain")
            encoding = input_data.get("encoding", "utf-8")
            max_length = input_data.get("max_length", 1000)
            preserve_spaces = input_data.get("preserve_spaces", True)
            remove_punctuation = input_data.get("remove_punctuation", False)
            add_timestamp = input_data.get("add_timestamp", True)
            custom_delimiter = input_data.get("custom_delimiter", " ")
            metadata = input_data.get("metadata", {})
            
            # Process text based on operation
            processed_text = self._apply_operation(
                text, operation, preserve_spaces, remove_punctuation
            )
            
            # Apply length limit
            if len(processed_text) > max_length:
                processed_text = processed_text[:max_length]
            
            # Add timestamp if requested
            if add_timestamp:
                from datetime import datetime, timezone
                timestamp = datetime.now(timezone.utc).isoformat() + "Z"
                processed_text = f"[{timestamp}] {processed_text}"
            
            # Prepare result
            result_data = {
                "original_text": text,
                "processed_text": processed_text,
                "operation": operation,
                "language": language,
                "format": format_type,
                "encoding": encoding,
                "length": len(processed_text),
                "metadata": metadata,
                "processing_options": {
                    "max_length": max_length,
                    "preserve_spaces": preserve_spaces,
                    "remove_punctuation": remove_punctuation,
                    "add_timestamp": add_timestamp,
                    "custom_delimiter": custom_delimiter,
                },
            }
            
            # Send result via webhook
            await self.webhook_service.send_webhook(
                webhook_url=webhook_url,
                payload=StepResult(
                    step=StepResultStep(id=step_id),
                    operation=OperationId(operation_id=operation_id),
                    variables=variables or {},
                    outputs=[StepResultOutput(data=result_data)],
                ),
            )
            
            logger.info(
                "Text processing completed",
                step_id=str(step_id),
                operation_id=str(operation_id),
            )
            
        except Exception as e:
            logger.error(
                "Text processing failed",
                step_id=str(step_id),
                operation_id=str(operation_id),
                error=str(e),
                exc_info=True,
            )
            
            # Send error via webhook
            try:
                await self.webhook_service.send_webhook(
                    webhook_url=webhook_url,
                    payload=StepResult(
                        step=StepResultStep(id=step_id),
                        operation=OperationId(operation_id=operation_id),
                        variables=variables or {},
                        outputs=[StepResultOutput(data={"error": str(e)})],
                    ),
                )
            except Exception as webhook_error:
                logger.error(
                    "Failed to send error webhook",
                    step_id=str(step_id),
                    operation_id=str(operation_id),
                    webhook_error=str(webhook_error),
                )
    
    def _apply_operation(
        self,
        text: str,
        operation: str,
        preserve_spaces: bool,
        remove_punctuation: bool,
    ) -> str:
        """Apply text processing operation."""
        import string
        
        # Remove punctuation if requested
        if remove_punctuation:
            text = text.translate(str.maketrans("", "", string.punctuation))
        
        # Apply operation
        if operation == "uppercase":
            result = text.upper()
        elif operation == "lowercase":
            result = text.lower()
        elif operation == "reverse":
            result = text[::-1]
        elif operation == "title":
            result = text.title()
        elif operation == "capitalize":
            result = text.capitalize()
        elif operation == "strip":
            result = text.strip()
        elif operation == "word_count":
            words = text.split() if preserve_spaces else text.split()
            result = str(len(words))
        elif operation == "char_count":
            result = str(len(text))
        else:
            # Default to uppercase
            result = text.upper()
        
        return result


# Initialize text processing service
text_service = TextProcessingService(webhook_service)


@router.post(
    "/example/process-text",
    summary="Process Text",
    description="Process text with maximum flexibility - example endpoint",
    tags=["Example"],
)
async def process_text(
    request: StepCall,
    background_tasks: BackgroundTasks,
) -> Response:
    """Process text with maximum flexibility."""
    
    # Model validation happens automatically by FastAPI before this function is called
    # If validation fails, FastAPI will return 422 before reaching this point
    
    # Generate operation ID
    from uuid import uuid4
    operation_id = uuid4()
    
    # Log request
    log_request(
        logger=logger,
        method="POST",
        path="/example/process-text",
        operation_id=str(operation_id),
    )
    
    # Log operation start
    log_operation_start(
        logger=logger,
        operation_id=str(operation_id),
        endpoint="/example/process-text",
    )
    
    # Add background task for processing
    background_tasks.add_task(
        text_service.process_text,
        step_id=request.step.id,
        operation_id=operation_id,
        webhook_url=str(request.webhook.url),
        input_data=request.initial.input,
        variables=request.variables,
    )
    
    # Return immediate response with operation ID
    response = Response(status_code=status.HTTP_202_ACCEPTED)
    response.headers["X-Operation-ID"] = str(operation_id)
    
    return response
