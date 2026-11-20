# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class BatchCriterion(BaseModel):
    """
    The flow fields to match. Keeps every field it gets. Known match fields, each a list of strings: port, protocol, tcp_flags, asn, lasthop_as_name, nexthop_asn, nexthop_as_name, nexthop, bgp_aspath, bgp_community, mac, country, vlans, device_name, device_type, site, interface_name.
    """

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "extra": "allow",
    }

    direction: Optional[str] = Field(
        validation_alias="direction",
        default=None,
        description="src, dst, or either (the default). Populators only; the API ignores it for tags.",
    )

    addr: Optional[List[str]] = Field(
        validation_alias="addr",
        default=None,
        description="IP addresses or CIDRs to match.",
    )
