# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .IdentityPredicateIdentityList import IdentityPredicateIdentityList


class IdentityPredicate(BaseModel):
    """
    IdentityPredicate model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    in_: Optional[IdentityPredicateIdentityList] = Field(
        validation_alias="in", serialization_alias="in", default=None
    )
