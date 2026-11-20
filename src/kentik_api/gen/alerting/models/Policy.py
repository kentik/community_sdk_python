# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .EventPolicySettings import EventPolicySettings
from .FlowPolicySettings import FlowPolicySettings
from .NmsPolicySettings import NmsPolicySettings
from .PolicyPolicyErrorInfo import PolicyPolicyErrorInfo
from .PolicyPolicyLevel import PolicyPolicyLevel
from .Source import Source


class Policy(BaseModel):
    """
    Policy model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    source: Optional[Source] = Field(validation_alias="source", default=None)

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="The time when the policy was created.",
    )

    modifiedAt: Optional[str] = Field(
        validation_alias="modifiedAt",
        default=None,
        description="The time when the policy was last modified.",
    )

    createdBy: Optional[str] = Field(
        validation_alias="createdBy",
        default=None,
        description="The user who created the policy.",
    )

    modifiedBy: Optional[str] = Field(
        validation_alias="modifiedBy",
        default=None,
        description="The user who last modified the policy.",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="The name of the policy."
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="The description of the policy.",
    )

    enabled: Optional[bool] = Field(
        validation_alias="enabled",
        default=None,
        description="provide annotation for default value\n\nWhether the policy is enabled.",
    )

    levels: Optional[List[Optional[PolicyPolicyLevel]]] = Field(
        validation_alias="levels",
        default=None,
        description="in future labels will be supported\n\nThe policy levels configuration.",
    )

    flow: Optional[FlowPolicySettings] = Field(validation_alias="flow", default=None)

    nms: Optional[NmsPolicySettings] = Field(validation_alias="nms", default=None)

    event: Optional[EventPolicySettings] = Field(validation_alias="event", default=None)

    hasErrors: Optional[bool] = Field(
        validation_alias="hasErrors",
        default=None,
        description="Whether the policy has errors in the run-time.",
    )

    lastError: Optional[PolicyPolicyErrorInfo] = Field(
        validation_alias="lastError", default=None
    )

    expireDate: Optional[str] = Field(
        validation_alias="expireDate",
        default=None,
        description="Indicates when the policy that was made from a query should expire and become disabled.",
    )
