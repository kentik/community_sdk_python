# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Filter import Filter


class FilterGroup(BaseModel):
    """
    A group of filters.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    connector: Optional[str] = Field(
        validation_alias="connector",
        default=None,
        description="How the filters combine: All (and) or Any (or).",
    )

    not_: Optional[bool] = Field(
        validation_alias="not",
        serialization_alias="not",
        default=None,
        description="Excludes the matching traffic instead of including it.",
    )

    filters: Optional[List[Optional[Filter]]] = Field(
        validation_alias="filters", default=None
    )
