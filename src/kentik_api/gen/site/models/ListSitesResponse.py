# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Site import Site


class ListSitesResponse(BaseModel):
    """
    ListSitesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    sites: Optional[List[Optional[Site]]] = Field(
        validation_alias="sites",
        default=None,
        description="List of configurations of requested sites",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
