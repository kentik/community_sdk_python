# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .EventPolicyLevelSettings import EventPolicyLevelSettings
from .FlowPolicyLevelSettings import FlowPolicyLevelSettings
from .NmsPolicyLevelSettings import NmsPolicyLevelSettings
from .NotificationChannelAssociation import NotificationChannelAssociation
from .Severity import Severity


class PolicyPolicyLevel(BaseModel):
    """
    PolicyPolicyLevel model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    severity: Optional[Severity] = Field(validation_alias="severity", default=None)

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The description of the policy level.",
    )

    ackRequired: Optional[bool] = Field(
        validation_alias="ackRequired",
        default=None,
        description="Whether acknowledgment is required for alerts that match this policy level.",
    )

    nms: Optional[NmsPolicyLevelSettings] = Field(validation_alias="nms", default=None)

    flow: Optional[FlowPolicyLevelSettings] = Field(
        validation_alias="flow", default=None
    )

    event: Optional[EventPolicyLevelSettings] = Field(
        validation_alias="event", default=None
    )

    notifications: Optional[List[Optional[NotificationChannelAssociation]]] = Field(
        validation_alias="notifications",
        default=None,
        description="The notification channel associations for this policy level. When the alert is triggered at this level, the channels are used to send the alert notification.",
    )
