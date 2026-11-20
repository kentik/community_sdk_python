# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class GetTraceForTestRequest(BaseModel):
    """
    GetTraceForTestRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="ID of test for which to retrieve network path trace data",
    )

    startTime: str = Field(
        validation_alias="startTime",
        description="Timestamp of the oldest results to include in results",
    )

    endTime: str = Field(
        validation_alias="endTime",
        description="Timestamp of the newest results to include in results",
    )

    agentIds: Optional[List[str]] = Field(
        validation_alias="agentIds",
        default=None,
        description="List of agent IDs from which to return results",
    )

    targetIps: Optional[List[str]] = Field(
        validation_alias="targetIps",
        default=None,
        description="List of target IP addresses for which to retrieve results",
    )
