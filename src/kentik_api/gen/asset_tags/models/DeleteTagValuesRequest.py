# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field

from .AssetType import AssetType


class DeleteTagValuesRequest(BaseModel):
    """
    DeleteTagValuesRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagId: str = Field(validation_alias="tagId", description="Tag key id")

    assetType: AssetType = Field(validation_alias="assetType")

    assetIds: List[str] = Field(validation_alias="assetIds", description="Asset ids")
