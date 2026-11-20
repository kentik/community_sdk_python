# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ChannelType import ChannelType


class NotificationChannel(BaseModel):
    """
    NotificationChannel
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier of the channel",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="User selected name of the channel",
    )

    type: Optional[ChannelType] = Field(validation_alias="type", default=None)

    enabled: Optional[bool] = Field(
        validation_alias="enabled", default=None, description="Administrative status"
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )
