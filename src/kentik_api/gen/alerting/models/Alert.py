# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AlertAcknowledgement import AlertAcknowledgement
from .AlertState import AlertState
from .ExternalContext import ExternalContext
from .FlowContext import FlowContext
from .NmsContext import NmsContext
from .Severity import Severity
from .Source import Source


class Alert(BaseModel):
    """
    Alert model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID (UUID format) of the alert.",
    )

    source: Optional[Source] = Field(validation_alias="source", default=None)

    startTimeAt: Optional[str] = Field(
        validation_alias="startTimeAt",
        default=None,
        description="The start time of the alert.",
    )

    endTimeAt: Optional[str] = Field(
        validation_alias="endTimeAt",
        default=None,
        description="The end time of the alert.",
    )

    state: Optional[AlertState] = Field(validation_alias="state", default=None)

    severity: Optional[Severity] = Field(validation_alias="severity", default=None)

    highestSeverity: Optional[Severity] = Field(
        validation_alias="highestSeverity", default=None
    )

    acknowledgement: Optional[AlertAcknowledgement] = Field(
        validation_alias="acknowledgement", default=None
    )

    eventStartTimeAt: Optional[str] = Field(
        validation_alias="eventStartTimeAt",
        default=None,
        description="The timestamp of the first trigger event that caused an alert to eventually activate.",
    )

    flow: Optional[FlowContext] = Field(validation_alias="flow", default=None)

    nms: Optional[NmsContext] = Field(validation_alias="nms", default=None)

    mitigationId: Optional[str] = Field(
        validation_alias="mitigationId",
        default=None,
        description="ID of the associated mitigation, if applicable.",
    )

    externalContexts: Optional[List[Optional[ExternalContext]]] = Field(
        validation_alias="externalContexts",
        default=None,
        description="External contexts attached to the alert (e.g. ServiceNow).",
    )
