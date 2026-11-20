# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TaskResults import TaskResults


class AgentResults(BaseModel):
    """
    AgentResults
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agentId: Optional[str] = Field(
        validation_alias="agentId",
        default=None,
        description="ID of the agent providing results",
    )

    health: Optional[str] = Field(
        validation_alias="health",
        default=None,
        description="Overall health status of all task for the test executed by this agent",
    )

    tasks: Optional[List[Optional[TaskResults]]] = Field(
        validation_alias="tasks",
        default=None,
        description="List of results for individual tasks",
    )
