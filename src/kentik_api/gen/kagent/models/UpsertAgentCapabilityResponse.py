# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AgentCapability import AgentCapability


class UpsertAgentCapabilityResponse(BaseModel):
    """
    UpsertAgentCapabilityResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capability: Optional[AgentCapability] = Field(
        validation_alias="capability", default=None
    )
