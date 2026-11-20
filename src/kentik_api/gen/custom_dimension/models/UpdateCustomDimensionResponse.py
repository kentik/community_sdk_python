# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CustomDimension import CustomDimension


class UpdateCustomDimensionResponse(BaseModel):
    """
    UpdateCustomDimensionResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dimension: Optional[CustomDimension] = Field(
        validation_alias="dimension", default=None
    )
