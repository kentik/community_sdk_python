# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .GroupedAlertSetting import GroupedAlertSetting


class GroupedAlertSettings(BaseModel):
    """
    GroupedAlertSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    default: Optional[GroupedAlertSetting] = Field(
        validation_alias="default", default=None
    )

    overrides: Optional[List[Optional[GroupedAlertSetting]]] = Field(
        validation_alias="overrides",
        default=None,
        description="Overrides to default grouped alerting settings",
    )
