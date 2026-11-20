# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AgentMetadataIpValue import AgentMetadataIpValue


class AgentMetadata(BaseModel):
    """
    AgentMetadata
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    privateIpv4Addresses: Optional[List[Optional[AgentMetadataIpValue]]] = Field(
        validation_alias="privateIpv4Addresses",
        default=None,
        description="List of private IPv4 addresses",
    )

    publicIpv4Addresses: Optional[List[Optional[AgentMetadataIpValue]]] = Field(
        validation_alias="publicIpv4Addresses",
        default=None,
        description="List of public IPv4 addresses",
    )

    privateIpv6Addresses: Optional[List[Optional[AgentMetadataIpValue]]] = Field(
        validation_alias="privateIpv6Addresses",
        default=None,
        description="List of private IPv6 addresses",
    )

    publicIpv6Addresses: Optional[List[Optional[AgentMetadataIpValue]]] = Field(
        validation_alias="publicIpv6Addresses",
        default=None,
        description="List of public IPv6 addresses",
    )

    staticIpv4: Optional[bool] = Field(
        validation_alias="staticIpv4",
        default=None,
        description="Indicates whether the agent's public IPv4 address is static (does not change).",
    )

    staticIpv6: Optional[bool] = Field(
        validation_alias="staticIpv6",
        default=None,
        description="Indicates whether the agent's public IPv6 address is static (does not change).",
    )
