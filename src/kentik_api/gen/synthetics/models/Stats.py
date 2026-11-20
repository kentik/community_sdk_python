# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Stats(BaseModel):
    """
    Stats
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    average: Optional[int] = Field(
        validation_alias="average", default=None, description="Average value"
    )

    min: Optional[int] = Field(
        validation_alias="min", default=None, description="Minimum value"
    )

    max: Optional[int] = Field(
        validation_alias="max", default=None, description="Maximum value"
    )
