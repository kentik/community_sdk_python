# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """
    AgentConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    created: Optional[str] = Field(
        validation_alias="created", default=None, description="Creation timestamp."
    )

    edited: Optional[str] = Field(
        validation_alias="edited",
        default=None,
        description="Last-modification timestamp.",
    )

    siteId: Optional[str] = Field(
        validation_alias="siteId",
        default=None,
        description="ID of the site the agent is assigned to.",
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

    osDistribution: Optional[str] = Field(
        validation_alias="osDistribution",
        default=None,
        description="override the OS distribution discovered by the agent\n\nOverride of the OS distribution discovered by the agent.",
    )
