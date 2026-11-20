# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AttributeFilter import AttributeFilter
from .SimpleAttributeFilter import SimpleAttributeFilter


class KeyValueFilter(BaseModel):
    """
    KeyValueFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    key: Optional[SimpleAttributeFilter] = Field(validation_alias="key", default=None)

    value: Optional[AttributeFilter] = Field(validation_alias="value", default=None)
