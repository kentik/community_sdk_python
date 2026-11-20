# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .v202309AlertingType import v202309AlertingType
from .v202309GroupedAlertSettings import v202309GroupedAlertSettings


class v202309AlertingSettings(BaseModel):
    """
    AlertingSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    disableWarningNotifications: Optional[bool] = Field(
        validation_alias="disableWarningNotifications",
        default=None,
        description="Boolean indicating whether to disable warning-level alert notifications",
    )

    alertingType: Optional[v202309AlertingType] = Field(
        validation_alias="alertingType", default=None
    )

    groupedAlertSettings: Optional[v202309GroupedAlertSettings] = Field(
        validation_alias="groupedAlertSettings", default=None
    )
