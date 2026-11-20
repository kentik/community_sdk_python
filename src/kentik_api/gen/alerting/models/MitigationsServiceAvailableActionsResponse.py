# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions import (
    MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions,
)


class MitigationsServiceAvailableActionsResponse(BaseModel):
    """
    MitigationsServiceAvailableActionsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    transitions: Optional[
        List[
            Optional[
                MitigationsServiceAvailableActionsResponseMitigationAvailableTransitions
            ]
        ]
    ] = Field(
        validation_alias="transitions",
        default=None,
        description="The available state transitions for mitigations.",
    )
