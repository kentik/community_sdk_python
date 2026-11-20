# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionTrafficRateBytes(BaseModel):
    """
    FlowspecActionTrafficRateBytes specifies the maximum traffic rate
    in bytes per second.

    Extended Community type and sub-type: 0x8006
    https://datatracker.ietf.org/doc/html/rfc8955#traffic_rate_in_bytes
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bytesPerSecond: Optional[float] = Field(
        validation_alias="bytesPerSecond",
        default=None,
        description="bytes_per_second must be greater than 0.\n\nSee FlowspecActionDiscard for discarding traffic.",
    )
