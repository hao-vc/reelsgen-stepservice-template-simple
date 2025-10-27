"""Operations API endpoint."""

from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Response, status
from fastapi.responses import JSONResponse

from app.logging_config import get_logger, log_request, log_operation_start
from app.schemas.operations import OperationRequest
from app.services.alert_service import AlertService
from app.services.operation_service import OperationService
from app.services.webhook_service import WebhookService

logger = get_logger(__name__)
router = APIRouter()

# Initialize services
webhook_service = WebhookService()
alert_service = AlertService()
operation_service = OperationService(webhook_service)


@router.post(
    "/operations/process",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Process Operation",
    description="Process an operation and send result via webhook",
    tags=["Operations"],
)
async def process_operation(
    request: OperationRequest,
    background_tasks: BackgroundTasks,
) -> Response:
    """Process an operation asynchronously."""
    
    # Generate operation ID
    operation_id = operation_service.generate_operation_id()
    
    # Log request
    log_request(
        logger=logger,
        method="POST",
        path="/operations/process",
        operation_id=str(operation_id),
    )
    
    # Log operation start
    log_operation_start(
        logger=logger,
        operation_id=str(operation_id),
        endpoint="/operations/process",
    )
    
    # Add background task for processing
    background_tasks.add_task(
        operation_service.process_operation,
        operation_id=operation_id,
        data=request.data,
        webhook_url=str(request.webhook_url),
    )
    
    # Return immediate response with operation ID
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.headers["X-Operation-ID"] = str(operation_id)
    
    return response
