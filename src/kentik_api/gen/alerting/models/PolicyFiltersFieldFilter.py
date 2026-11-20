# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .PolicyFiltersOperator import PolicyFiltersOperator


class PolicyFiltersFieldFilter(BaseModel):
    """
    PolicyFiltersFieldFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    field: Optional[str] = Field(
        validation_alias="field",
        default=None,
        description="The field the filter is applied to.",
    )

    operator: Optional[PolicyFiltersOperator] = Field(
        validation_alias="operator", default=None
    )

    value: Optional[str] = Field(
        validation_alias="value",
        default=None,
        description="The right-hand value used for the filter operation.",
    )
