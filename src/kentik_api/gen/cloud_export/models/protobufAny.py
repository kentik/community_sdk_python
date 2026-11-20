# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class protobufAny(BaseModel):
    """
    protobufAny model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[str] = Field(
        validation_alias="@type", serialization_alias="@type", default=None
    )
