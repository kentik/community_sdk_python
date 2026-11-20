# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GetLatestDeviceConfigurationsResponse(BaseModel):
    """
    GetLatestDeviceConfigurationsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    configs: Optional[Dict[str, Any]] = Field(
        validation_alias="configs",
        default=None,
        description="Map from device ID to latest configuration.",
    )
