# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .PolicyDimensionFiltersEntryStringArray import (
    PolicyDimensionFiltersEntryStringArray,
)


class PolicyDimensionFiltersEntry(BaseModel):
    """
    PolicyDimensionFiltersEntry model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not",
        serialization_alias="not",
        default=None,
        description="If true, the entry will be negated.",
    )

    dimension: Optional[str] = Field(
        validation_alias="dimension",
        default=None,
        description="The dimension the filter entry is applied to.",
    )

    equalsAny: Optional[PolicyDimensionFiltersEntryStringArray] = Field(
        validation_alias="equalsAny", default=None
    )

    matchesAny: Optional[PolicyDimensionFiltersEntryStringArray] = Field(
        validation_alias="matchesAny", default=None
    )
