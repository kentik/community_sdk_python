# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AgentMetadata import AgentMetadata
from .AgentStatus import AgentStatus
from .ImplementType import ImplementType
from .IPFamily import IPFamily


class Agent(BaseModel):
    """
    Agent
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier of the agent",
    )

    siteName: Optional[str] = Field(
        validation_alias="siteName",
        default=None,
        description="Name of the site where agent is located",
    )

    status: Optional[AgentStatus] = Field(validation_alias="status", default=None)

    alias: Optional[str] = Field(
        validation_alias="alias",
        default=None,
        description="User selected descriptive name of the agent",
    )

    type: Optional[str] = Field(
        validation_alias="type",
        default=None,
        description="Type of agent (global | private)",
    )

    os: Optional[str] = Field(
        validation_alias="os",
        default=None,
        description="OS version of server/VM hosting the agent",
    )

    ip: Optional[str] = Field(
        validation_alias="ip",
        default=None,
        description="Public IP address of the agent (auto-detected)",
    )

    lat: Optional[float] = Field(
        validation_alias="lat",
        default=None,
        description="Latitude of agent's location (signed decimal degrees)",
    )

    long: Optional[float] = Field(
        validation_alias="long",
        default=None,
        description="Longitude of agent's location (signed decimal degrees)",
    )

    lastAuthed: Optional[str] = Field(
        validation_alias="lastAuthed",
        default=None,
        description="Timestamp of the last authorization",
    )

    family: Optional[IPFamily] = Field(validation_alias="family", default=None)

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="ASN of the AS owning agent's public address",
    )

    siteId: Optional[str] = Field(
        validation_alias="siteId",
        default=None,
        description="ID of the site hosting the agent (if configured in Kentik)",
    )

    version: Optional[str] = Field(
        validation_alias="version",
        default=None,
        description="Software version of the agent",
    )

    city: Optional[str] = Field(
        validation_alias="city",
        default=None,
        description="City where the agent is located",
    )

    region: Optional[str] = Field(
        validation_alias="region",
        default=None,
        description="Geographical region of agent's location",
    )

    country: Optional[str] = Field(
        validation_alias="country",
        default=None,
        description="Country of agent's location",
    )

    testIds: Optional[List[str]] = Field(
        validation_alias="testIds",
        default=None,
        description="IDs of user's test running on the agent",
    )

    localIp: Optional[str] = Field(
        validation_alias="localIp",
        default=None,
        description="Internal IP address of the agent",
    )

    cloudRegion: Optional[str] = Field(
        validation_alias="cloudRegion",
        default=None,
        description="Cloud region (if any) hosting the agent",
    )

    cloudProvider: Optional[str] = Field(
        validation_alias="cloudProvider",
        default=None,
        description="Cloud provider (if any) hosting the agent",
    )

    agentImpl: Optional[ImplementType] = Field(
        validation_alias="agentImpl", default=None
    )

    labels: Optional[List[str]] = Field(
        validation_alias="labels",
        default=None,
        description="List of names of labels associated with the agent",
    )

    metadata: Optional[AgentMetadata] = Field(validation_alias="metadata", default=None)
