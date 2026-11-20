# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MeasurementSchema(BaseModel):
    """
    MeasurementSchema model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[int] = Field(validation_alias="id", default=None)

    entityType: Optional[str] = Field(validation_alias="entityType", default=None)

    description: Optional[str] = Field(validation_alias="description", default=None)

    appProtocol: Optional[int] = Field(validation_alias="appProtocol", default=None)

    sourceTimestampColumn: Optional[str] = Field(
        validation_alias="sourceTimestampColumn", default=None
    )

    dimensions: Optional[Dict[str, Any]] = Field(
        validation_alias="dimensions", default=None
    )

    metrics: Optional[Dict[str, Any]] = Field(validation_alias="metrics", default=None)

    lastSeen: Optional[str] = Field(validation_alias="lastSeen", default=None)

    tags: Optional[List[str]] = Field(validation_alias="tags", default=None)
