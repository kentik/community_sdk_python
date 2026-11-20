# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AssetType import AssetType


class TagValue(BaseModel):
    """
    TagValue
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagId: Optional[str] = Field(
        validation_alias="tagId", default=None, description="Tag key id"
    )

    assetType: Optional[AssetType] = Field(validation_alias="assetType", default=None)

    assetId: Optional[str] = Field(
        validation_alias="assetId", default=None, description="Tag asset id"
    )

    value: Optional[str] = Field(
        validation_alias="value", default=None, description="Tag value"
    )
