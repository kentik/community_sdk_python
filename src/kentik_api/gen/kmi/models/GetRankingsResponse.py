# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Ranking import Ranking


class GetRankingsResponse(BaseModel):
    """
    GetRankingsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    rankings: Optional[List[Optional[Ranking]]] = Field(
        validation_alias="rankings", default=None, description="List of rankings"
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
