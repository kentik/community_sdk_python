# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationState import MitigationState
from .MitigationStateEntry import MitigationStateEntry
from .MitigationTarget import MitigationTarget
from .MitigationType import MitigationType
from .Source import Source


class Mitigation(BaseModel):
    """
    Mitigation model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="The ID of the mitigation."
    )

    type: Optional[MitigationType] = Field(validation_alias="type", default=None)

    alarmIds: Optional[List[str]] = Field(
        validation_alias="alarmIds",
        default=None,
        description="The alarm IDs associated with this mitigation.",
    )

    target: Optional[MitigationTarget] = Field(validation_alias="target", default=None)

    currentState: Optional[MitigationState] = Field(
        validation_alias="currentState", default=None
    )

    previousState: Optional[MitigationState] = Field(
        validation_alias="previousState", default=None
    )

    platformId: Optional[str] = Field(
        validation_alias="platformId",
        default=None,
        description="The mitigation platform ID the mitigation is derived from.",
    )

    methodId: Optional[str] = Field(
        validation_alias="methodId",
        default=None,
        description="The mitigation method ID the mitigation is derived from.",
    )

    startTimeAt: Optional[str] = Field(
        validation_alias="startTimeAt",
        default=None,
        description="The time when the mitigation started.",
    )

    endTimeAt: Optional[str] = Field(
        validation_alias="endTimeAt",
        default=None,
        description="The time when the mitigation ended or will end.",
    )

    states: Optional[List[Optional[MitigationStateEntry]]] = Field(
        validation_alias="states",
        default=None,
        description="The history of state changes for the mitigation.",
    )

    autoStopTtl: Optional[str] = Field(
        validation_alias="autoStopTtl",
        default=None,
        description="The automatic stop time-to-live for the mitigation.",
    )

    comment: Optional[str] = Field(
        validation_alias="comment",
        default=None,
        description="A comment describing the mitigation.",
    )

    source: Optional[Source] = Field(validation_alias="source", default=None)
