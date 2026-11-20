# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionMarkDSCP(BaseModel):
    """
    FlowspecActionMarkDSCP instructs a system to modify the DSCP bits in the IP header.

    Extended Community type and sub-type: 0x8009
    https://datatracker.ietf.org/doc/html/rfc8955#traffic_marking_subtype
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dscp: Optional[int] = Field(validation_alias="dscp", default=None)
