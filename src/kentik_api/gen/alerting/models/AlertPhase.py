# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowContext import FlowContext
from .NmsContext import NmsContext
from .Severity import Severity


class AlertPhase(BaseModel):
    """
    AlertPhase model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    severity: Optional[Severity] = Field(validation_alias="severity", default=None)

    startTimeAt: Optional[str] = Field(
        validation_alias="startTimeAt",
        default=None,
        description="The start time of the alert phase.",
    )

    endTimeAt: Optional[str] = Field(
        validation_alias="endTimeAt",
        default=None,
        description="The end time of the alert phase.",
    )

    flow: Optional[FlowContext] = Field(validation_alias="flow", default=None)

    nms: Optional[NmsContext] = Field(validation_alias="nms", default=None)
