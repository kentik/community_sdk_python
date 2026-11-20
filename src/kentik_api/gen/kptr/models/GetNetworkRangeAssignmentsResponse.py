# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class GetNetworkRangeAssignmentsResponse(BaseModel):
    """
    GetNetworkRangeAssignmentsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    networkRanges: Optional[List[str]] = Field(
        validation_alias="networkRanges",
        default=None,
        description="IP prefixes (e.g., 10.0.0.0/8) that this agent is responsible for performing lookups for",
    )
