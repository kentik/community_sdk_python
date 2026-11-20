# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .NotificationChannel import NotificationChannel


class GetNotificationChannelResponse(BaseModel):
    """
    GetNotificationChannelResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    notificationChannel: Optional[NotificationChannel] = Field(
        validation_alias="notificationChannel", default=None
    )
