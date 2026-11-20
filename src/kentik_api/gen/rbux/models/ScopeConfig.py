# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SavedFilterFilters import SavedFilterFilters
from .ScopeDimensions import ScopeDimensions


class ScopeConfig(BaseModel):
    """
    ScopeConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dimensions: Optional[ScopeDimensions] = Field(
        validation_alias="dimensions", default=None
    )

    filters: Optional[SavedFilterFilters] = Field(
        validation_alias="filters", default=None
    )
