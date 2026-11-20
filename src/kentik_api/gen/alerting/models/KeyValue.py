# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class KeyValue(BaseModel):
    """
    KeyValue model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    value: Optional[Dict[str, Any]] = Field(validation_alias="value", default=None)
