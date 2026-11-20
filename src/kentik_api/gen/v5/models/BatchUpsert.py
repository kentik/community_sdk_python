# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BatchCriterion import BatchCriterion


class BatchUpsert(BaseModel):
    """
    A value and the criteria that set it.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    value: str = Field(
        validation_alias="value", description="The tag name, or the populator value."
    )

    criteria: Optional[List[Optional[BatchCriterion]]] = Field(
        validation_alias="criteria",
        default=None,
        description="Each criterion defines one tag or populator with this value.",
    )
