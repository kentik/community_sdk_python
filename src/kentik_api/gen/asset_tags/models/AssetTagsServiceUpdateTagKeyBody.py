# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AssetTagsServiceUpdateTagKeyBody(BaseModel):
    """
    UpdateTagKeyRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    displayName: Optional[str] = Field(
        validation_alias="displayName", default=None, description="Tag key display name"
    )

    color: Optional[str] = Field(
        validation_alias="color", default=None, description="Tag key hex color"
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="Tag key description"
    )
