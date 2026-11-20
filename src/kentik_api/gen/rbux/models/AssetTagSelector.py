# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class AssetTagSelector(BaseModel):
    """
    AssetTagSelector
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tagId: str = Field(
        validation_alias="tagId", description="Asset tag key identifier."
    )

    values: Optional[List[str]] = Field(
        validation_alias="values",
        default=None,
        description="Asset tag values to match for the given tag key.",
    )
