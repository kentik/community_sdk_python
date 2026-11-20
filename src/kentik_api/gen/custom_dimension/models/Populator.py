# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Populator(BaseModel):
    """
    Populator model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the populator.",
    )

    value: Optional[str] = Field(
        validation_alias="value",
        default=None,
        description="The value of the dimension. When the custom dimension's type is 'string' - Valid characters: alphanumeric, spaces, dashes and underscores. Length: min=1, max=128. When the custom dimension's type is 'uint32' - Valid values: min=0, max=4294967295.",
    )

    direction: Optional[str] = Field(
        validation_alias="direction",
        default=None,
        description="The direction of the populator. Valid values: 'src', 'dst', or 'either'.",
    )

    deviceName: Optional[List[str]] = Field(
        validation_alias="deviceName",
        default=None,
        description="Device names, IPs, or regular expressions. A match results when any specified device name matches the device name or IP address associated with a device sending flow data.",
    )

    deviceType: Optional[List[str]] = Field(
        validation_alias="deviceType",
        default=None,
        description="Device types or regular expressions. A match results when any specified device type matches the device_type associated with a device sending flow data.",
    )

    site: Optional[List[str]] = Field(
        validation_alias="site",
        default=None,
        description="Site names or regular expressions. A match results when any specified site matches the site associated with a device sending flow data.",
    )

    interfaceName: Optional[List[str]] = Field(
        validation_alias="interfaceName",
        default=None,
        description="Interface names or regular expressions. A match results when any specified interface name matches the name or description of an interface sending flow data.",
    )

    addr: Optional[List[str]] = Field(
        validation_alias="addr",
        default=None,
        description="IP addresses in IP/CIDR format. A match results when any specified IP address corresponds to a range of IP addresses in incoming flow. It allows IPv6 CIDRs. 'short form' (e.g. 1::2/127) is allowed. If no CIDRs are specified in a tag, the tag will be matched against both incoming IPv4 and v6 flows. If CIDRs are given, the tag will only be matched against the given type of flow; in particular, if you only give IPv4 CIDRs, the tag will not match any IPv6 flows, and vice versa.",
    )

    port: Optional[List[int]] = Field(
        validation_alias="port",
        default=None,
        description="Ports (between 0 and 65535). A match results when any specified port matches a port number in incoming flow.",
    )

    tcpFlags: Optional[int] = Field(
        validation_alias="tcpFlags",
        default=None,
        description="TCP flag: Numbers between 0 and 255 representing an 8-bit binary bit pattern corresponding to TCP flags. A match will result if the value in both the flow bit pattern and the bitmask is 1 at any of the eight places.",
    )

    protocol: Optional[List[int]] = Field(
        validation_alias="protocol",
        default=None,
        description="Protocol numbers (between 0 and 255). A match results when any specified protocol number is the same as the protocol of the traffic represented by the flow.",
    )

    asn: Optional[List[int]] = Field(
        validation_alias="asn",
        default=None,
        description="Last-hop (origin) ASN: ASNs (between 1 and 2^32-1=4294967295). A match results when any specified ASN is the same as the last ASN in the path in the routing table for either the source (SRC IP) or destination (DST IP).",
    )

    lasthopAsName: Optional[List[str]] = Field(
        validation_alias="lasthopAsName",
        default=None,
        description="Last-hop (origin) AS Name: AS Names or regular expressions. A match results when any specified AS Name represents the name corresponding to the last ASN in the path in the routing table for either the source (SRC IP) or destination (DST IP).",
    )

    nexthopAsn: Optional[List[int]] = Field(
        validation_alias="nexthopAsn",
        default=None,
        description="Next-hop ASN. A match results when any specified ASN is the same as the ASN of the next hop router based on AS path.",
    )

    nexthopAsName: Optional[List[str]] = Field(
        validation_alias="nexthopAsName",
        default=None,
        description="Next-hop AS Name: AS Names or regular expressions. A match results when any specified ASN represents the name corresponding to the ASN of the next hop router based on AS path.",
    )

    nexthop: Optional[List[str]] = Field(
        validation_alias="nexthop",
        default=None,
        description="Next-hop IP: IPv4 and/or IPv6 CIDRs. A match results when any specified IP is within a range of specified IPv4 and/or IPv6 CIDRs.",
    )

    bgpAspath: Optional[List[str]] = Field(
        validation_alias="bgpAspath",
        default=None,
        description="BGP AS path: Numbers representing bgp aspath. A match results when any specified value is the same as the BGP AS-PATH in the route. Example: '^3737 1212,_7801_,2906$' would look for any of those 3 combinations in the AS path. Permitted characters []*:_^$.0123456789()+?,space-",
    )

    bgpCommunity: Optional[List[str]] = Field(
        validation_alias="bgpCommunity",
        default=None,
        description="BGP community: Numbers or regular expression representing BGP community (i.e. 2096:2212). A match results when any specified value is the same as the BGP community of the BGP route associated with incoming flow data. Permitted characters []*:_^$.0123456789()+?,space-",
    )

    mac: Optional[List[str]] = Field(
        validation_alias="mac",
        default=None,
        description="MAC Addresses. A match results when any specified MAC Address matches source or destination Ethernet (L2) address.",
    )

    country: Optional[List[str]] = Field(
        validation_alias="country",
        default=None,
        description="Country: Two-character country codes. A match results when any specified country code matches source or destination country of the flow.",
    )

    vlans: Optional[List[str]] = Field(
        validation_alias="vlans",
        default=None,
        description="VLAN(s): Integers or ranges of integers between 0 and 4095.",
    )

    user: Optional[str] = Field(
        validation_alias="user",
        default=None,
        description="The system-assigned ID of the user who created the populator.",
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Date-time of populator creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Date-time of most-recent populator edit, in UTC.",
    )

    addrCount: Optional[int] = Field(
        validation_alias="addrCount",
        default=None,
        description="Number of IP addresses.",
    )

    macCount: Optional[int] = Field(
        validation_alias="macCount",
        default=None,
        description="Number of MAC addresses.",
    )

    extendedFields: Optional[Dict[str, Any]] = Field(
        validation_alias="extendedFields",
        default=None,
        description="Additional fields set on object but not currently available on API.",
    )
