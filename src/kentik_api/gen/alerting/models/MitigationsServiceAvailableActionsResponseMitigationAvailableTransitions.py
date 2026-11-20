# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationActionDetail import MitigationActionDetail
from .MitigationState import MitigationState


class MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions(
    BaseModel
):
    """
    MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    fromState: Optional[MitigationState] = Field(
        validation_alias="fromState", default=None
    )

    availableActions: Optional[List[Optional[MitigationActionDetail]]] = Field(
        validation_alias="availableActions",
        default=None,
        description="The available actions from this state.",
    )
