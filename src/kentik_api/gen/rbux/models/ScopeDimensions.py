# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AssetTagSelector import AssetTagSelector


class ScopeDimensions(BaseModel):
    """
    ScopeDimensions
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    sites: Optional[List[str]] = Field(
        validation_alias="sites",
        default=None,
        description="Site identifiers included in the scope.",
    )

    labels: Optional[List[str]] = Field(
        validation_alias="labels",
        default=None,
        description="Label identifiers included in the scope.",
    )

    assetTags: Optional[List[Optional[AssetTagSelector]]] = Field(
        validation_alias="assetTags",
        default=None,
        description="Customer-defined asset tag selectors included in the scope.",
    )
