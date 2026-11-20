# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TagKey import TagKey


class ListTagKeysResponse(BaseModel):
    """
    ListTagKeysResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagKeys: Optional[List[Optional[TagKey]]] = Field(
        validation_alias="tagKeys", default=None, description="Tag keys"
    )
