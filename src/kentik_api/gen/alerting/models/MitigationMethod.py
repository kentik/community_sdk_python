# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationPlatformType import MitigationPlatformType
from .NotificationChannelAssociation import NotificationChannelAssociation


class MitigationMethod(BaseModel):
    """
    MitigationMethod model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The ID of the mitigation method.",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="The name of the mitigation method.",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The description of the mitigation method.",
    )

    ackRequired: Optional[bool] = Field(
        validation_alias="ackRequired",
        default=None,
        description="Whether acknowledgment is required before applying this mitigation method.",
    )

    excludedIpCidrs: Optional[List[str]] = Field(
        validation_alias="excludedIpCidrs",
        default=None,
        description="The IP/CIDR ranges that are excluded from this mitigation method.",
    )

    gracePeriod: Optional[str] = Field(
        validation_alias="gracePeriod",
        default=None,
        description="The grace period before the mitigation method is applied.",
    )

    type: Optional[MitigationPlatformType] = Field(
        validation_alias="type", default=None
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The time when the mitigation method was created.",
    )

    modifiedAt: Optional[str] = Field(
        validation_alias="modifiedAt",
        default=None,
        description="The time when the mitigation method was last modified.",
    )

    notifications: Optional[List[Optional[NotificationChannelAssociation]]] = Field(
        validation_alias="notifications",
        default=None,
        description="The notification channel associations for this mitigation method.",
    )
