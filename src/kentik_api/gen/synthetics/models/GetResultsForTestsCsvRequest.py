# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class GetResultsForTestsCsvRequest(BaseModel):
    """
    GetResultsForTestsCsvRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ids: List[str] = Field(
        validation_alias="ids",
        description="List of test IDs for which to retrieve results",
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

    aggregate: Optional[bool] = Field(
        validation_alias="aggregate",
        default=None,
        description="If true, retrieve result aggregated across the requested time period, else return complete time series",
    )
