# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BgpMetricType import BgpMetricType
from .Nlri import Nlri


class GetMetricsForTargetRequest(BaseModel):
    """
    GetMetricsForTargetRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    startTime: str = Field(
        validation_alias="startTime",
        description="UTC timestamp of the beginning of queried interval",
    )

    endTime: str = Field(
        validation_alias="endTime",
        description="UTC timestamp of the end of queried interval",
    )

    target: Nlri = Field(validation_alias="target")

    includeCovered: Optional[bool] = Field(
        validation_alias="includeCovered",
        default=None,
        description="Return metrics for subnets (sub-prefixes) of the target prefix (default: false)",
    )

    metrics: List[BgpMetricType] = Field(
        validation_alias="metrics",
        description="List of one or more BGP metric types to return",
    )
