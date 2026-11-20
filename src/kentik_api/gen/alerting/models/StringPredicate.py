# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .StringPredicateStringList import StringPredicateStringList


class StringPredicate(BaseModel):
    """
    StringPredicate model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    contains: Optional[str] = Field(validation_alias="contains", default=None)

    startsWith: Optional[str] = Field(validation_alias="startsWith", default=None)

    endsWith: Optional[str] = Field(validation_alias="endsWith", default=None)

    matchesRegex: Optional[str] = Field(validation_alias="matchesRegex", default=None)

    in_: Optional[StringPredicateStringList] = Field(
        validation_alias="in", serialization_alias="in", default=None
    )
