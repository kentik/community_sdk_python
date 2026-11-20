# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Location import Location


class NetNode(BaseModel):
    """
    NetNode
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    ip: Optional[str] = Field(
        validation_alias="ip",
        default=None,
        description="IP address of the node in standard textual notation",
    )

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="AS number owning the address of the node",
    )

    asName: Optional[str] = Field(
        validation_alias="asName",
        default=None,
        description="Name of the AS owning the address of the node",
    )

    location: Optional[Location] = Field(validation_alias="location", default=None)

    dnsName: Optional[str] = Field(
        validation_alias="dnsName",
        default=None,
        description="DNS name of the node (obtained by reverse DNS resolution)",
    )

    deviceId: Optional[str] = Field(
        validation_alias="deviceId",
        default=None,
        description="ID of the device corresponding with the node in Kentik configuration",
    )

    siteId: Optional[str] = Field(
        validation_alias="siteId",
        default=None,
        description="ID of the site containing the device corresponding with the node in Kentik configuration",
    )
