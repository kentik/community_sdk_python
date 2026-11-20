# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowPolicyLevelSettingsConditionsOperator import (
    FlowPolicyLevelSettingsConditionsOperator,
)


class ConditionsForecastCondition(BaseModel):
    """
    ConditionsForecastCondition model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    operator: Optional[FlowPolicyLevelSettingsConditionsOperator] = Field(
        validation_alias="operator", default=None
    )

    percentageValue: Optional[str] = Field(
        validation_alias="percentageValue", default=None
    )
