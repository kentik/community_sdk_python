# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .BaseUnit import BaseUnit
from .FieldDataType import FieldDataType
from .FieldDirection import FieldDirection


class MetricField(BaseModel):
    """
    A field that represents a measurable metric in a query.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    key: Optional[str] = Field(
        validation_alias="key", default=None, description="Field key used in queries"
    )

    label: Optional[str] = Field(
        validation_alias="label",
        default=None,
        description="Human-readable display name",
    )

    dataType: Optional[FieldDataType] = Field(validation_alias="dataType", default=None)

    category: Optional[str] = Field(
        validation_alias="category",
        default=None,
        description="Category used for grouping in the UI",
    )

    column: Optional[str] = Field(
        validation_alias="column",
        default=None,
        description="Underlying storage column name, if applicable",
    )

    direction: Optional[FieldDirection] = Field(
        validation_alias="direction", default=None
    )

    inverse: Optional[str] = Field(
        validation_alias="inverse",
        default=None,
        description="Key of the inverse direction field, if any",
    )

    values: Optional[Dict[str, Any]] = Field(
        validation_alias="values",
        default=None,
        description="Enumerated value map for enum-typed fields",
    )

    lastSeen: Optional[str] = Field(
        validation_alias="lastSeen",
        default=None,
        description="ISO-8601 timestamp of when this field was last observed, if available",
    )

    windowFn: Optional[str] = Field(
        validation_alias="windowFn",
        default=None,
        description="Window function applied during aggregation, if any",
    )

    aggregateFn: Optional[str] = Field(
        validation_alias="aggregateFn",
        default=None,
        description="Aggregation function applied to this metric, if any",
    )

    expression: Optional[str] = Field(
        validation_alias="expression",
        default=None,
        description="Computed expression used to derive this metric, if any",
    )

    dependsOn: Optional[List[str]] = Field(
        validation_alias="dependsOn",
        default=None,
        description="Keys of other metrics this metric depends on",
    )

    toBits: Optional[bool] = Field(
        validation_alias="toBits",
        default=None,
        description="When true, the metric value should be converted to bits",
    )

    rollup: Optional[bool] = Field(
        validation_alias="rollup",
        default=None,
        description="When true, the metric supports rollup aggregation",
    )

    healthyValue: Optional[str] = Field(
        validation_alias="healthyValue",
        default=None,
        description="The value considered healthy for this metric (may be numeric or categorical)",
    )

    familyKey: Optional[str] = Field(
        validation_alias="familyKey",
        default=None,
        description="Key of the MetricFamilyDef this metric belongs to",
    )

    baseUnit: Optional[BaseUnit] = Field(validation_alias="baseUnit", default=None)

    shared: Optional[bool] = Field(
        validation_alias="shared",
        default=None,
        description="When true, the metric can be used in child measurements",
    )
