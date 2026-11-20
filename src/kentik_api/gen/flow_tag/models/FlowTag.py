# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AddressInfo import AddressInfo


class FlowTag(BaseModel):
    """
    FlowTag
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique system assigned identifier of the flow tag",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="This will appear in places where selecting a tag is necessary",
    )

    editedBy: Optional[str] = Field(
        validation_alias="editedBy",
        default=None,
        description="User who last edited this tag",
    )

    createdBy: Optional[str] = Field(
        validation_alias="createdBy",
        default=None,
        description="User who created this tag",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate",
        default=None,
        description="Date and time when this tag was created",
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Date and time when this tag was last updated",
    )

    ip: Optional[AddressInfo] = Field(validation_alias="ip", default=None)

    port: Optional[List[str]] = Field(
        validation_alias="port",
        default=None,
        description="Port number associated with the flow tag",
    )

    tcpFlags: Optional[int] = Field(
        validation_alias="tcpFlags",
        default=None,
        description="TCP flags associated with the flow tag",
    )

    protocol: Optional[List[int]] = Field(
        validation_alias="protocol",
        default=None,
        description="Protocol numbers associated with the flow tag",
    )

    deviceName: Optional[List[str]] = Field(
        validation_alias="deviceName",
        default=None,
        description="Name of the device associated with the flow tag",
    )

    deviceType: Optional[List[str]] = Field(
        validation_alias="deviceType",
        default=None,
        description="Type of the device associated with the flow tag",
    )

    site: Optional[List[str]] = Field(
        validation_alias="site",
        default=None,
        description="Site where the device associated with the flow tag is located",
    )

    interfaceName: Optional[List[str]] = Field(
        validation_alias="interfaceName",
        default=None,
        description="Name of the interface associated with the flow tag",
    )

    asn: Optional[List[str]] = Field(
        validation_alias="asn",
        default=None,
        description="Autonomous System Number (ASN) associated with the flow tag",
    )

    lasthopAsName: Optional[List[str]] = Field(
        validation_alias="lasthopAsName",
        default=None,
        description="Name of the last hop's Autonomous System (AS) associated with the flow tag",
    )

    nexthopAsn: Optional[List[str]] = Field(
        validation_alias="nexthopAsn",
        default=None,
        description="Autonomous System Number (ASN) of the next hop associated with the flow tag",
    )

    nexthopAsName: Optional[List[str]] = Field(
        validation_alias="nexthopAsName",
        default=None,
        description="Name of the next hop's Autonomous System (AS) associated with the flow tag",
    )

    nexthop: Optional[List[str]] = Field(
        validation_alias="nexthop",
        default=None,
        description="Next hop associated with the flow tag",
    )

    bgpAspath: Optional[List[str]] = Field(
        validation_alias="bgpAspath",
        default=None,
        description="BGP AS path associated with the flow tag",
    )

    bgpCommunity: Optional[List[str]] = Field(
        validation_alias="bgpCommunity",
        default=None,
        description="BGP community associated with the flow tag",
    )

    mac: Optional[AddressInfo] = Field(validation_alias="mac", default=None)

    country: Optional[List[str]] = Field(
        validation_alias="country",
        default=None,
        description="Country associated with the flow tag",
    )

    vlans: Optional[List[str]] = Field(
        validation_alias="vlans",
        default=None,
        description="VLANs associated with the flow tag",
    )
