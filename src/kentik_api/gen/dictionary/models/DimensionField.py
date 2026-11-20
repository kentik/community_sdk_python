# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from .FieldDataType import FieldDataType
from .FieldDirection import FieldDirection
from .OperatorSetKey import OperatorSetKey


class DimensionField(BaseModel):
    """
    A field that can be used as a dimension/filter in a query.
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

    operatorSetKey: Optional[OperatorSetKey] = Field(
        validation_alias="operatorSetKey", default=None
    )

    filterOnly: Optional[bool] = Field(
        validation_alias="filterOnly",
        default=None,
        description="When true, the field may only be used as a filter, not a group-by dimension",
    )

    filterColumn: Optional[str] = Field(
        validation_alias="filterColumn",
        default=None,
        description="Alternative column name used when this field is applied as a filter",
    )

    queryColumn: Optional[str] = Field(
        validation_alias="queryColumn",
        default=None,
        description="Alternative column name used when this field is used in a query group-by",
    )

    canCount: Optional[bool] = Field(
        validation_alias="canCount",
        default=None,
        description="When true, the field can be used with WINDOW_FUNCTION_COUNT",
    )

    shared: Optional[bool] = Field(
        validation_alias="shared",
        default=None,
        description="When true, the field can be used in child measurements",
    )
