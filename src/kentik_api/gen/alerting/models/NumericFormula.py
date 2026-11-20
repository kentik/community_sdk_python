# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .NumericPredicateGroup import NumericPredicateGroup


class NumericFormula(BaseModel):
    """
    NumericFormula model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    or_: Optional[List[Optional[NumericPredicateGroup]]] = Field(
        validation_alias="or", serialization_alias="or", default=None
    )
