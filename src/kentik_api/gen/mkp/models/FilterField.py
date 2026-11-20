# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FilterField(BaseModel):
    """
    FilterField
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    filterField: Optional[str] = Field(validation_alias="filterField", default=None)

    operator: Optional[str] = Field(validation_alias="operator", default=None)

    filterValue: Optional[str] = Field(validation_alias="filterValue", default=None)
