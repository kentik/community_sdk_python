# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field


class PermissionEntry(BaseModel):
    """
    PermissionEntry
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capability: str = Field(
        validation_alias="capability",
        description="String identifying capability that is granted of denied",
    )

    allowed: bool = Field(
        validation_alias="allowed",
        description="Flag indicating whether operation is allowed",
    )
