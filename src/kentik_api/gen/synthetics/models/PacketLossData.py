# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class PacketLossData(BaseModel):
    """
    PacketLossData
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    current: Optional[float] = Field(
        validation_alias="current",
        default=None,
        description="Current packet loss value",
    )

    health: Optional[str] = Field(
        validation_alias="health",
        default=None,
        description="Health evaluation status for the metric (healthy | warning | critical)",
    )
