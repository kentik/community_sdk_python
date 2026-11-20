# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Agent import Agent
from .BootstrapInfo import BootstrapInfo


class CreateAgentResponse(BaseModel):
    """
    CreateAgentResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agent: Optional[Agent] = Field(validation_alias="agent", default=None)

    bootstrap: Optional[BootstrapInfo] = Field(
        validation_alias="bootstrap", default=None
    )
