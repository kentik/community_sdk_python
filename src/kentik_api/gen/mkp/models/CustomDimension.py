# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CustomDimension(BaseModel):
    """
    CustomDimension
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dimension: Optional[str] = Field(validation_alias="dimension", default=None)

    populator: Optional[str] = Field(validation_alias="populator", default=None)
