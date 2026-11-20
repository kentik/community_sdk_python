# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ConditionsBaselineCondition import ConditionsBaselineCondition
from .ConditionsForecastCondition import ConditionsForecastCondition
from .ConditionsInterfaceCapacityCondition import ConditionsInterfaceCapacityCondition
from .ConditionsRatioCondition import ConditionsRatioCondition
from .ConditionsStaticCondition import ConditionsStaticCondition
from .ConditionsTopKeysCondition import ConditionsTopKeysCondition


class FlowPolicyLevelSettingsConditions(BaseModel):
    """
    FlowPolicyLevelSettingsConditions model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    static: Optional[ConditionsStaticCondition] = Field(
        validation_alias="static", default=None
    )

    baseline: Optional[ConditionsBaselineCondition] = Field(
        validation_alias="baseline", default=None
    )

    topKeys: Optional[ConditionsTopKeysCondition] = Field(
        validation_alias="topKeys", default=None
    )

    interfaceCapacity: Optional[ConditionsInterfaceCapacityCondition] = Field(
        validation_alias="interfaceCapacity", default=None
    )

    ratio: Optional[ConditionsRatioCondition] = Field(
        validation_alias="ratio", default=None
    )

    forecast: Optional[ConditionsForecastCondition] = Field(
        validation_alias="forecast", default=None
    )
