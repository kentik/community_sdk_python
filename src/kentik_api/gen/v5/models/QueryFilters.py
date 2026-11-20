# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FilterGroup import FilterGroup


class QueryFilters(BaseModel):
    """
    The ad hoc filters of a query.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    connector: Optional[str] = Field(
        validation_alias="connector",
        default=None,
        description="How the filter groups combine: All (and) or Any (or).",
    )

    filterGroups: Optional[List[Optional[FilterGroup]]] = Field(
        validation_alias="filterGroups", default=None
    )
