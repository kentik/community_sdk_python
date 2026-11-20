# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Agent import Agent


class GetAgentResponse(BaseModel):
    """
    GetAgentResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agent: Optional[Agent] = Field(validation_alias="agent", default=None)
