# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AgentConfig import AgentConfig
from .InstallConfig import InstallConfig


class AgentServiceUpdateAgentBody(BaseModel):
    """
    AgentServiceUpdateAgentBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    running: Optional[bool] = Field(
        validation_alias="running",
        default=None,
        description="agent is actively sending heartbeats\n\nIndication whether the agent is actively sending heartbeats.",
    )

    clusterId: Optional[str] = Field(
        validation_alias="clusterId",
        default=None,
        description="ID of the cluster the agent belongs to.",
    )

    publicKey: Optional[str] = Field(
        validation_alias="publicKey",
        default=None,
        description="PEM encoded public key\n\nPEM-encoded public key the agent authenticates with.",
    )

    provisioningToken: Optional[str] = Field(
        validation_alias="provisioningToken",
        default=None,
        description="Provisioning token the agent registered with.",
    )

    config: Optional[AgentConfig] = Field(validation_alias="config", default=None)

    install: Optional[InstallConfig] = Field(validation_alias="install", default=None)
