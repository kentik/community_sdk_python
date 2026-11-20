# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class BatchUpsertCounts(BaseModel):
    """
    Upsert counts so far.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    total: Optional[int] = Field(
        validation_alias="total",
        default=None,
        description="The sum of the other counts.",
    )

    applied: Optional[int] = Field(
        validation_alias="applied", default=None, description="Values applied."
    )

    invalid: Optional[int] = Field(
        validation_alias="invalid", default=None, description="Values not valid."
    )

    unchanged: Optional[int] = Field(
        validation_alias="unchanged",
        default=None,
        description="Values that changed nothing.",
    )

    over_limit: Optional[int] = Field(
        validation_alias="over_limit",
        default=None,
        description="Values ignored because they exceed the contract limit.",
    )
