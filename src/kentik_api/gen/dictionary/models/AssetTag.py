# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AssetTag(BaseModel):
    """
    User defined tags that can be assigned to devices
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="Unique identifier for the asset tag",
    )

    displayName: Optional[str] = Field(
        validation_alias="displayName",
        default=None,
        description="Human-readable display name",
    )
