# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FlowPolicyLevelSettingsActivationSettings import (
    FlowPolicyLevelSettingsActivationSettings,
)
from .FlowPolicyLevelSettingsConditions import FlowPolicyLevelSettingsConditions
from .FlowPolicyLevelSettingsMitigationAssociation import (
    FlowPolicyLevelSettingsMitigationAssociation,
)


class FlowPolicyLevelSettings(BaseModel):
    """
    FlowPolicyLevelSettings model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    conditions: List[FlowPolicyLevelSettingsConditions] = Field(
        validation_alias="conditions",
        description="The conditions of the policy level settings.",
    )

    activation: Optional[FlowPolicyLevelSettingsActivationSettings] = Field(
        validation_alias="activation", default=None
    )

    mitigationAssociations: List[FlowPolicyLevelSettingsMitigationAssociation] = Field(
        validation_alias="mitigationAssociations",
        description="in future: dimension filters for sub-policies\n\nThe mitigation associations of the given policy level (when alert is activated with the level severity, these mitigation methods will be applied).",
    )
