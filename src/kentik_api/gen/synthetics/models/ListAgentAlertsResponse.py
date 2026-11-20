# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AgentAlert import AgentAlert


class ListAgentAlertsResponse(BaseModel):
    """
    ListAgentAlertsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agentAlerts: Optional[List[Optional[AgentAlert]]] = Field(
        validation_alias="agentAlerts", default=None
    )
