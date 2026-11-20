# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class AgentAlert(BaseModel):
    """
    AgentAlert model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(validation_alias="id", default=None)

    thresholdSeconds: Optional[int] = Field(
        validation_alias="thresholdSeconds", default=None
    )

    notificationChannelIds: Optional[List[str]] = Field(
        validation_alias="notificationChannelIds", default=None
    )

    agentId: Optional[str] = Field(validation_alias="agentId", default=None)

    agentName: Optional[str] = Field(validation_alias="agentName", default=None)
