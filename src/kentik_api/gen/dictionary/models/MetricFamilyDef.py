# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BaseUnit import BaseUnit
from .MetricQuantity import MetricQuantity


class MetricFamilyDef(BaseModel):
    """
    Definition of a metric family grouping related metrics by quantity and unit.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    key: Optional[str] = Field(
        validation_alias="key",
        default=None,
        description="Unique identifier for the metric family",
    )

    label: Optional[str] = Field(
        validation_alias="label",
        default=None,
        description="Human-readable display name",
    )

    quantity: Optional[MetricQuantity] = Field(
        validation_alias="quantity", default=None
    )

    baseUnit: Optional[BaseUnit] = Field(validation_alias="baseUnit", default=None)

    dualAxisCompatible: Optional[List[str]] = Field(
        validation_alias="dualAxisCompatible",
        default=None,
        description="Metric family keys compatible for dual-axis rendering",
    )

    incompatibleWith: Optional[List[str]] = Field(
        validation_alias="incompatibleWith",
        default=None,
        description="Metric family keys that cannot be combined with this family",
    )
