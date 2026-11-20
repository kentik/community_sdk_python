# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AgentResults import AgentResults


class TestResults(BaseModel):
    """
    TestResults
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    testId: Optional[str] = Field(
        validation_alias="testId",
        default=None,
        description="ID of the test for which results are provided",
    )

    time: Optional[str] = Field(
        validation_alias="time", default=None, description="Results timestamp (UTC)"
    )

    health: Optional[str] = Field(
        validation_alias="health", default=None, description="Health status of the test"
    )

    agents: Optional[List[Optional[AgentResults]]] = Field(
        validation_alias="agents",
        default=None,
        description="List of results from agents executing tasks on behalf of the test",
    )
