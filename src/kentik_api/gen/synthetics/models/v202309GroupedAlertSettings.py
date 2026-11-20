# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .v202309GroupedAlertSetting import v202309GroupedAlertSetting


class v202309GroupedAlertSettings(BaseModel):
    """
    GroupedAlertSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    default: Optional[v202309GroupedAlertSetting] = Field(
        validation_alias="default", default=None
    )

    overrides: Optional[List[Optional[v202309GroupedAlertSetting]]] = Field(
        validation_alias="overrides",
        default=None,
        description="Overrides to default grouped alerting settings",
    )
