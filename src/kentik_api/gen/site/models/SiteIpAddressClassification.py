# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class SiteIpAddressClassification(BaseModel):
    """
    SiteIpAddressClassification
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    infrastructureNetworks: Optional[List[str]] = Field(
        validation_alias="infrastructureNetworks",
        default=None,
        description="List of IP address prefixes (in standard CIDR notation) used in infrastructure networks",
    )

    userAccessNetworks: Optional[List[str]] = Field(
        validation_alias="userAccessNetworks",
        default=None,
        description="List of IP address prefixes (in standard CIDR notation) used in access networks",
    )

    otherNetworks: Optional[List[str]] = Field(
        validation_alias="otherNetworks",
        default=None,
        description="List of IP address prefixes (in standard CIDR notation) used in other networks",
    )
