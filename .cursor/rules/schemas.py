"""Step schemas."""

from typing import Any
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel


# OPERATION SCHEMAS

class OperationId(BaseModel):
    """Operation ID."""

    operation_id: UUID


# STEP CALL SCHEMAS
class StepCallPreviousResult(BaseModel):
    """Step call previous result."""

    output: dict[str, Any]


class StepCallInitial(BaseModel):
    """Step call initial."""

    input: dict[str, Any]


class StepCallStep(BaseModel):
    """Step call step."""

    id: UUID


class StepWebhook(BaseModel):
    """Webhook."""

    url: AnyHttpUrl


class StepCall(BaseModel):
    """Step call."""

    step: StepCallStep
    webhook: StepWebhook
    previous: StepCallPreviousResult | None = None
    initial: StepCallInitial
    variables: dict[str, Any]


# STEP RESULT SCHEMAS


class StepResultStep(BaseModel):
    """Step result step."""

    id: UUID


class StepResultOutput(BaseModel):
    """Step result output."""

    data: dict[str, Any]


class StepResult(BaseModel):
    """Step result."""

    step: StepResultStep
    operation: OperationId
    variables: dict[str, Any]
    outputs: list[StepResultOutput]


# FINAL STEP RESPONSE SCHEMAS


class FinalStepResultVideoThumbnail(BaseModel):
    """Final step result video thumbnail."""

    url: AnyHttpUrl


class FinalStepResultVideoChannel(BaseModel):
    """Final step result video channel."""

    id: UUID


class FinalStepResultVideo(BaseModel):
    """Final step result video."""

    url: AnyHttpUrl
    thumbnail: FinalStepResultVideoThumbnail
    channel: FinalStepResultVideoChannel
    description: str


class FinalStepResultStep(BaseModel):
    """Final step result step."""

    id: UUID


class FinalStepResult(BaseModel):
    """Final step result."""

    step: FinalStepResultStep
    operation: OperationId
    videos: list[FinalStepResultVideo]
