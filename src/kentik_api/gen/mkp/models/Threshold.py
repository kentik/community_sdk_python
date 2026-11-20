# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Activate import Activate
from .Condition import Condition
from .Mitigation import Mitigation
from .NotificationChannel import NotificationChannel


class Threshold(BaseModel):
    """
    Threshold
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(validation_alias="id", default=None)

    activate: Optional[Activate] = Field(validation_alias="activate", default=None)

    severity: Optional[str] = Field(validation_alias="severity", default=None)

    conditions: Optional[List[Optional[Condition]]] = Field(
        validation_alias="conditions", default=None
    )

    mitigations: Optional[List[Optional[Mitigation]]] = Field(
        validation_alias="mitigations", default=None
    )

    notificationChannels: Optional[List[Optional[NotificationChannel]]] = Field(
        validation_alias="notificationChannels", default=None
    )

    thresholdAckRequired: Optional[bool] = Field(
        validation_alias="thresholdAckRequired", default=None
    )

    enableTenantNotifications: Optional[bool] = Field(
        validation_alias="enableTenantNotifications", default=None
    )

    receiveLandlordNotifications: Optional[bool] = Field(
        validation_alias="receiveLandlordNotifications", default=None
    )
