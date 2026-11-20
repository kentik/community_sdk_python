# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowContextMetricValue(BaseModel):
    """
    FlowContextMetricValue model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="The name of the metric value (e.g. 'bytes_in', 'bytes_out', 'packets_in', 'packets_out', etc.).",
    )

    value: Optional[float] = Field(
        validation_alias="value",
        default=None,
        description="The value of the given metric.",
    )
