# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PolicyDimensionFiltersEntry import PolicyDimensionFiltersEntry


class PolicyDimensionFiltersConjunction(BaseModel):
    """
    PolicyDimensionFiltersConjunction model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    entries: Optional[List[Optional[PolicyDimensionFiltersEntry]]] = Field(
        validation_alias="entries",
        default=None,
        description="The entries of the conjunction.",
    )
