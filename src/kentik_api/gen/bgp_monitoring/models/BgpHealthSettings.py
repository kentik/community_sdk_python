# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class BgpHealthSettings(BaseModel):
    """
    BgpHealthSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    reachabilityWarning: Optional[float] = Field(
        validation_alias="reachabilityWarning",
        default=None,
        description="Threshold (in percents) for triggering warning level alert",
    )

    reachabilityCritical: Optional[float] = Field(
        validation_alias="reachabilityCritical",
        default=None,
        description="Threshold (in percents) for triggering critical level alert",
    )
