# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionIPNextHopCopy(BaseModel):
    """
    FlowspecActionIPNextHopCopy allows the traffic to be copied
    to a specific Next Hop IP address.

    Extended Community type and sub-type: 0x0800 with least-significant bit 'C' set to 1

    The target next-hop address refers to the 'Network Address of Next-Hop' field
    of the associated NLRI.
    https://datatracker.ietf.org/doc/html/draft-simpson-idr-flowspec-redirect
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    nextHop: Optional[str] = Field(
        validation_alias="nextHop",
        default=None,
        description="IPv4 or IPv6 address to copy to",
    )
