# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CloudSubnet import CloudSubnet


class NetworkClass(BaseModel):
    """
    NetworkClass model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    internalAsns: Optional[List[str]] = Field(
        validation_alias="internalAsns", default=None, description="Internal ASNs"
    )

    internalIps: Optional[List[str]] = Field(
        validation_alias="internalIps", default=None, description="Internal IPs"
    )

    usePrivateAsns: Optional[bool] = Field(
        validation_alias="usePrivateAsns",
        default=None,
        description="Specify to use internal ASNs",
    )

    usePrivateSubnets: Optional[bool] = Field(
        validation_alias="usePrivateSubnets",
        default=None,
        description="Specify to use internal IPs",
    )

    cloudSubnets: Optional[List[Optional[CloudSubnet]]] = Field(
        validation_alias="cloudSubnets",
        default=None,
        description="Cloud provider and subnet info.",
    )
