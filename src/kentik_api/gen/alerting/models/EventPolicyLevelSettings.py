# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .PolicyDimensionFilters import PolicyDimensionFilters


class EventPolicyLevelSettings(BaseModel):
    """
    EventPolicyLevelSettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filters: Optional[PolicyDimensionFilters] = Field(
        validation_alias="filters", default=None
    )
