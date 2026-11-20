# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FieldBy import FieldBy
from .SortingConfigOrder import SortingConfigOrder


class SortingConfigField(BaseModel):
    """
    SortingConfigField model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    by: Optional[FieldBy] = Field(validation_alias="by", default=None)

    order: Optional[SortingConfigOrder] = Field(validation_alias="order", default=None)
