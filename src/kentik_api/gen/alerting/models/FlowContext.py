# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .FlowContextActivationStatus import FlowContextActivationStatus
from .FlowContextMetricValue import FlowContextMetricValue


class FlowContext(BaseModel):
    """
    FlowContext model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    metricValues: Optional[List[Optional[FlowContextMetricValue]]] = Field(
        validation_alias="metricValues",
        default=None,
        description="The metric values of the alert determined by the policy configuration.",
    )

    activationStatus: Optional[FlowContextActivationStatus] = Field(
        validation_alias="activationStatus", default=None
    )

    baselineValue: Optional[float] = Field(
        validation_alias="baselineValue",
        default=None,
        description="The baseline value used when activating the alert.",
    )

    alertKeyDetails: Optional[Dict[str, Any]] = Field(
        validation_alias="alertKeyDetails",
        default=None,
        description="The alert key details of the alert: each key might be expanded into multiple details.",
    )
