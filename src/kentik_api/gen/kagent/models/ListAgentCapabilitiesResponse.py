# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AgentCapability import AgentCapability


class ListAgentCapabilitiesResponse(BaseModel):
    """
    ListAgentCapabilitiesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capabilities: Optional[List[Optional[AgentCapability]]] = Field(
        validation_alias="capabilities",
        default=None,
        description="List of agent capability objects.",
    )
