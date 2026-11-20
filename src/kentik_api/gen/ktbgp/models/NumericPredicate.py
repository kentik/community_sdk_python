# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NumericOp import NumericOp


class NumericPredicate(BaseModel):
    """
    NumericPredicate model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    operator: Optional[NumericOp] = Field(validation_alias="operator", default=None)

    value: Optional[str] = Field(validation_alias="value", default=None)
