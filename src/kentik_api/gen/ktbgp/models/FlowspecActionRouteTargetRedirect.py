# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionRouteTargetRedirect(BaseModel):
    """
    FlowspecActionRouteTargetRedirect allows the traffic to be redirected to a VRF
    routing instance that lists the specified route-target in its import policy.

    Depending on the contents of the message, this will be encoded as:
    Extended Community type and sub-type: 0x8008 (2-octet ASN)
    or
    Extended Community type and sub-type: 0x8208 (4-octet ASN)
    https://datatracker.ietf.org/doc/html/rfc8955#rt_redirect_action_subtype
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="If 32 bits are used for the ASN, the route target can only be 16 bits long",
    )

    routeTarget: Optional[int] = Field(
        validation_alias="routeTarget",
        default=None,
        description="If 32 bits are used for the route target, the asn can only be 16 bits long",
    )
