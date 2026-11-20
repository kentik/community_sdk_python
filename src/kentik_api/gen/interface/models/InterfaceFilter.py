# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ConnectivityType import ConnectivityType
from .IpFilter import IpFilter
from .NetworkBoundary import NetworkBoundary


class InterfaceFilter(BaseModel):
    """
    Supports multiple search criteria. Fields are combined to AND statements to perform search.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    text: Optional[str] = Field(
        validation_alias="text",
        default=None,
        description="Search text match in interface description and alias.",
    )

    deviceIds: Optional[List[str]] = Field(
        validation_alias="deviceIds", default=None, description="Search by device ID."
    )

    connectivityTypes: Optional[List[Optional[ConnectivityType]]] = Field(
        validation_alias="connectivityTypes",
        default=None,
        description="Search by type of interface connectivity.",
    )

    networkBoundaries: Optional[List[Optional[NetworkBoundary]]] = Field(
        validation_alias="networkBoundaries",
        default=None,
        description="Search by type of network boundary.",
    )

    providers: Optional[List[str]] = Field(
        validation_alias="providers", default=None, description="Search by provider"
    )

    snmpSpeeds: Optional[List[int]] = Field(
        validation_alias="snmpSpeeds", default=None, description="SNMP speed in Mbps"
    )

    ipTypes: Optional[List[Optional[IpFilter]]] = Field(
        validation_alias="ipTypes", default=None, description="Search by ip address."
    )
