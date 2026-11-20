# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AgentRegistration(BaseModel):
    """
    AgentRegistration
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    publicKey: Optional[str] = Field(
        validation_alias="publicKey",
        default=None,
        description="PEM-encoded public key the agent authenticates with.",
    )

    siteId: Optional[str] = Field(
        validation_alias="siteId",
        default=None,
        description="ID of the site to assign the agent to.",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="User-friendly name of the agent.",
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Description of the agent.",
    )

    releaseChannel: Optional[str] = Field(
        validation_alias="releaseChannel",
        default=None,
        description="Release channel the agent takes software updates from.",
    )

    clusterId: Optional[str] = Field(
        validation_alias="clusterId",
        default=None,
        description="ID of the cluster to assign the agent to.",
    )
