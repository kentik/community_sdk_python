# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PathElement(BaseModel):
    """
    PathElement model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[str] = Field(validation_alias="type", default=None)

    value: Optional[str] = Field(validation_alias="value", default=None)

    region: Optional[str] = Field(validation_alias="region", default=None)
