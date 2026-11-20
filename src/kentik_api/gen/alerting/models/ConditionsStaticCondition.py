# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .FlowPolicyLevelSettingsConditionsOperator import (
    FlowPolicyLevelSettingsConditionsOperator,
)


class ConditionsStaticCondition(BaseModel):
    """
    ConditionsStaticCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    metric: str = Field(
        validation_alias="metric",
        description="The metric used for the policy level condition.",
    )

    operator: FlowPolicyLevelSettingsConditionsOperator = Field(
        validation_alias="operator"
    )

    value: float = Field(
        validation_alias="value",
        description="The value used for the policy level condition.",
    )
