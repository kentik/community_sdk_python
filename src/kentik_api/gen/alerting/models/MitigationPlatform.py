# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationPlatformType import MitigationPlatformType


class MitigationPlatform(BaseModel):
    """
    MitigationPlatform model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the mitigation platform.",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="The name of the mitigation platform.",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The description of the mitigation platform.",
    )

    type: Optional[MitigationPlatformType] = Field(
        validation_alias="type", default=None
    )

    mitigationMethodIds: Optional[List[str]] = Field(
        validation_alias="mitigationMethodIds",
        default=None,
        description="The mitigation method IDs associated with this platform.",
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The time when the mitigation platform was created.",
    )

    modifiedAt: Optional[str] = Field(
        validation_alias="modifiedAt",
        default=None,
        description="The time when the mitigation platform was last modified.",
    )
