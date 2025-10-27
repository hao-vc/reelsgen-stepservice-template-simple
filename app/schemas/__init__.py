"""Schemas package."""

from app.schemas.health import HealthResponse
from app.schemas.operations import (
    OperationRequest,
    OperationResponse,
    WebhookPayload,
)
from app.schemas.step_schemas import (
    FinalStepResult,
    FinalStepResultStep,
    FinalStepResultVideo,
    FinalStepResultVideoChannel,
    FinalStepResultVideoThumbnail,
    OperationId,
    StepCall,
    StepCallInitial,
    StepCallPreviousResult,
    StepCallStep,
    StepResult,
    StepResultOutput,
    StepResultStep,
    StepWebhook,
)

__all__ = [
    # Health
    "HealthResponse",
    # Operations
    "OperationRequest",
    "OperationResponse",
    "WebhookPayload",
    # Step schemas
    "OperationId",
    "StepCallPreviousResult",
    "StepCallInitial",
    "StepCallStep",
    "StepWebhook",
    "StepCall",
    "StepResultStep",
    "StepResultOutput",
    "StepResult",
    "FinalStepResultVideoThumbnail",
    "FinalStepResultVideoChannel",
    "FinalStepResultVideo",
    "FinalStepResultStep",
    "FinalStepResult",
]
