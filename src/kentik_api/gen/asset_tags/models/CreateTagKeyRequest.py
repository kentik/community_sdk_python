# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CreateTagKeyRequest(BaseModel):
    """
    CreateTagKeyRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: str = Field(validation_alias="name", description="Tag key name")

    displayName: Optional[str] = Field(
        validation_alias="displayName", default=None, description="Tag key display name"
    )

    color: Optional[str] = Field(
        validation_alias="color", default=None, description="Tag key hex color"
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="Tag key description"
    )
