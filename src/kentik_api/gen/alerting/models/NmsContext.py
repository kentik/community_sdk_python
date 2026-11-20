# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .NmsContextActivationInfo import NmsContextActivationInfo
from .NmsContextDatasetInfo import NmsContextDatasetInfo


class NmsContext(BaseModel):
    """
    in the comments are evm equivalents
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    activationInfo: Optional[NmsContextActivationInfo] = Field(
        validation_alias="activationInfo", default=None
    )

    datasetInfo: Optional[NmsContextDatasetInfo] = Field(
        validation_alias="datasetInfo", default=None
    )

    targets: Optional[Dict[str, Any]] = Field(
        validation_alias="targets", default=None, description="AlarmTargets"
    )

    metricValues: Optional[Dict[str, Any]] = Field(
        validation_alias="metricValues", default=None, description="AlarmMetrics"
    )

    previousMetricValues: Optional[Dict[str, Any]] = Field(
        validation_alias="previousMetricValues",
        default=None,
        description="AlarmPreviousStatus",
    )

    device: Optional[Dict[str, Any]] = Field(
        validation_alias="device", default=None, description="AlarmDevice"
    )

    groupKey: Optional[Dict[str, Any]] = Field(
        validation_alias="groupKey",
        default=None,
        description="AlarmGroupKey - for example: {device_id: 123, ifindex: 42} for an interface alarm OR {agent_id: 12} for an agent alarm\nsub-set of dimensions which all matches should include",
    )
