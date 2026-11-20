# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Condition(BaseModel):
    """
    Condition
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[str] = Field(validation_alias="type", default=None)

    value: Optional[str] = Field(validation_alias="value", default=None)

    metric: Optional[str] = Field(validation_alias="metric", default=None)

    operator: Optional[str] = Field(validation_alias="operator", default=None)

    valueType: Optional[str] = Field(validation_alias="valueType", default=None)

    valueSelect: Optional[str] = Field(validation_alias="valueSelect", default=None)
