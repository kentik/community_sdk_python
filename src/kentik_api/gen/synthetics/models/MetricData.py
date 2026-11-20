# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class MetricData(BaseModel):
    """
    MetricData
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    current: Optional[int] = Field(
        validation_alias="current", default=None, description="Current value of metric"
    )

    rollingAvg: Optional[int] = Field(
        validation_alias="rollingAvg",
        default=None,
        description="Rolling average of metric",
    )

    rollingStddev: Optional[int] = Field(
        validation_alias="rollingStddev",
        default=None,
        description="Rolling average of standard deviation of metric",
    )

    health: Optional[str] = Field(
        validation_alias="health",
        default=None,
        description="Health evaluation status for the metric (healthy | warning | critical)",
    )
