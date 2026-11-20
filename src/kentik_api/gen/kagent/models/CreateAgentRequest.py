# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AgentRegistration import AgentRegistration
from .RegistrationConfig import RegistrationConfig


class CreateAgentRequest(BaseModel):
    """
    CreateAgentRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agent: Optional[AgentRegistration] = Field(validation_alias="agent", default=None)

    config: Optional[RegistrationConfig] = Field(
        validation_alias="config", default=None
    )
