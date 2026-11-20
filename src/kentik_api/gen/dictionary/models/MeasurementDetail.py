# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DimensionField import DimensionField
from .MeasurementFamily import MeasurementFamily
from .MetricField import MetricField


class MeasurementDetail(BaseModel):
    """
    Full detail for a single measurement (e.g. a traffic flow table or NMS measurement).
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Internal measurement name"
    )

    displayName: Optional[str] = Field(
        validation_alias="displayName",
        default=None,
        description="Human-readable display name",
    )

    family: Optional[MeasurementFamily] = Field(validation_alias="family", default=None)

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Optional description of this measurement",
    )

    lastSeen: Optional[str] = Field(
        validation_alias="lastSeen",
        default=None,
        description="ISO-8601 timestamp of when this measurement was last observed, if available",
    )

    dimensions: Optional[List[Optional[DimensionField]]] = Field(
        validation_alias="dimensions",
        default=None,
        description="Dimension fields available for this measurement",
    )

    metrics: Optional[List[Optional[MetricField]]] = Field(
        validation_alias="metrics",
        default=None,
        description="Metric fields available for this measurement",
    )
