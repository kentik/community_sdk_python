# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class MitigationsServiceAvailableActionsForMitigationResponse(BaseModel):
    """
    MitigationsServiceAvailableActionsForMitigationResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    availableActions: Optional[List[str]] = Field(
        validation_alias="availableActions",
        default=None,
        description="The available actions for the mitigation.",
    )
