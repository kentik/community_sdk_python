# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .TagKey import TagKey


class UpdateTagKeyResponse(BaseModel):
    """
    UpdateTagKeyResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagKey: Optional[TagKey] = Field(validation_alias="tagKey", default=None)
