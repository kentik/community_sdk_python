# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AgentCapabilityServiceUpsertAgentCapabilityBody(BaseModel):
    """
    AgentCapabilityServiceUpsertAgentCapabilityBody model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bundleId: Optional[str] = Field(
        validation_alias="bundleId",
        default=None,
        description="ID of the bundle the capability software is taken from.",
    )

    enabled: Optional[bool] = Field(
        validation_alias="enabled",
        default=None,
        description="Indication whether the capability is enabled on the agent.",
    )

    version: Optional[str] = Field(
        validation_alias="version",
        default=None,
        description="Version of the capability to run.",
    )

    channel: Optional[str] = Field(
        validation_alias="channel",
        default=None,
        description="Release channel the capability takes software updates from.",
    )

    configId: Optional[str] = Field(
        validation_alias="configId",
        default=None,
        description="ID of the configuration applied to the capability.",
    )

    groupId: Optional[str] = Field(
        validation_alias="groupId",
        default=None,
        description="ID of the group the capability belongs to.",
    )

    groupIndex: Optional[int] = Field(
        validation_alias="groupIndex",
        default=None,
        description="Index of the capability within its group.",
    )
