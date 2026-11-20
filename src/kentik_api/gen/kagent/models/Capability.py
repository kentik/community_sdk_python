# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Capability(BaseModel):
    """
    Capability model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="The capability name: one of kagent, kproxy, ranger and so on.",
    )

    displayName: Optional[str] = Field(
        validation_alias="displayName",
        default=None,
        description="The capability display name",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The capability description",
    )

    seedBundleId: Optional[str] = Field(
        validation_alias="seedBundleId", default=None, description="The seed bundle ID"
    )

    seedConfig: Optional[str] = Field(
        validation_alias="seedConfig",
        default=None,
        description="The seed config for the capability",
    )
