# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .LookupField import LookupField
from .OrderDirection import OrderDirection


class OrderField(BaseModel):
    """
    OrderField
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    field: Optional[LookupField] = Field(validation_alias="field", default=None)

    direction: Optional[OrderDirection] = Field(
        validation_alias="direction", default=None
    )
