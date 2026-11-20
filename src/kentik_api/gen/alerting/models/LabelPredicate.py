# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .LabelPredicateStringList import LabelPredicateStringList


class LabelPredicate(BaseModel):
    """
    Matches repeated string fields such as device.labels and device.roles.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    in_: Optional[LabelPredicateStringList] = Field(
        validation_alias="in", serialization_alias="in", default=None
    )

    containsAll: Optional[LabelPredicateStringList] = Field(
        validation_alias="containsAll", default=None
    )
