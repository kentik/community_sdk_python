# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .NotificationChannel import NotificationChannel


class ListNotificationChannelsResponse(BaseModel):
    """
    ListNotificationChannelsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    notificationChannels: Optional[List[Optional[NotificationChannel]]] = Field(
        validation_alias="notificationChannels",
        default=None,
        description="List of notification channels",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries that were not included in the list (should be always zero)",
    )
