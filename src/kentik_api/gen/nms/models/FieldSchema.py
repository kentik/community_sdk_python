# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .FieldDisplay import FieldDisplay
from .FieldType import FieldType
from .Usage import Usage


class FieldSchema(BaseModel):
    """
    FieldSchema model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: Optional[FieldType] = Field(validation_alias="type", default=None)

    column: Optional[str] = Field(validation_alias="column", default=None)

    mask: Optional[str] = Field(validation_alias="mask", default=None)

    description: Optional[str] = Field(validation_alias="description", default=None)

    unit: Optional[str] = Field(validation_alias="unit", default=None)

    label: Optional[str] = Field(validation_alias="label", default=None)

    values: Optional[Dict[str, Any]] = Field(validation_alias="values", default=None)

    lastSeen: Optional[str] = Field(validation_alias="lastSeen", default=None)

    supportedUsages: Optional[List[Optional[Usage]]] = Field(
        validation_alias="supportedUsages", default=None
    )

    queryColumn: Optional[str] = Field(validation_alias="queryColumn", default=None)

    enrichment: Optional[str] = Field(validation_alias="enrichment", default=None)

    display: Optional[FieldDisplay] = Field(validation_alias="display", default=None)

    isPrimaryKey: Optional[bool] = Field(
        validation_alias="isPrimaryKey",
        default=None,
        description="note - only dimensions can be primary keys, not metrics",
    )
