# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel


class FlowspecActionDiscard(BaseModel):
    """
    FlowspecActionDiscard specifies that the traffic should be discarded.

    This is a special case of FlowspecActionTrafficRateBytes with 0 bytes per second.
    Extended Community type and sub-type: 0x8006
    https://datatracker.ietf.org/doc/html/rfc8955#traffic_rate_in_bytes
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}
