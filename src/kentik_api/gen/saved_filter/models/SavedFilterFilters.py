# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .SavedFilterFilterGroup import SavedFilterFilterGroup


class SavedFilterFilters(BaseModel):
    """
    SavedFilterFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    any: Optional[bool] = Field(
        validation_alias="any",
        default=None,
        description="Whether to require matches against ALL or ANY filter. Defaults to requiring a match for all.",
    )

    filterGroups: List[SavedFilterFilterGroup] = Field(
        validation_alias="filterGroups",
        description="Individual groups of filters. This allows matches of e.g. ANY(ALL(x), ANY(y)).",
    )
