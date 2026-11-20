# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationState import MitigationState
from .MitigationUserAction import MitigationUserAction


class MitigationActionDetail(BaseModel):
    """
    MitigationActionDetail model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    eventName: Optional[str] = Field(
        validation_alias="eventName",
        default=None,
        description="The name of the event that triggers this action.",
    )

    action: Optional[MitigationUserAction] = Field(
        validation_alias="action", default=None
    )

    actionDescription: Optional[str] = Field(
        validation_alias="actionDescription",
        default=None,
        description="The description of the action.",
    )

    fromState: Optional[MitigationState] = Field(
        validation_alias="fromState", default=None
    )

    toStates: Optional[List[Optional[MitigationState]]] = Field(
        validation_alias="toStates",
        default=None,
        description="The possible states the mitigation can transition to.",
    )
