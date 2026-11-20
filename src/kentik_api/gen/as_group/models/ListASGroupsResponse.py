# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ASGroupDetailed import ASGroupDetailed


class ListASGroupsResponse(BaseModel):
    """
    ListASGroupsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asGroups: Optional[List[Optional[ASGroupDetailed]]] = Field(
        validation_alias="asGroups",
        default=None,
        description="List of configurations of requested AS groups",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
