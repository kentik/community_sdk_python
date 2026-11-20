# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CustomColumnData(BaseModel):
    """
    CustomColumnData
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceId: Optional[str] = Field(
        validation_alias="deviceId", default=None, description="Device ID"
    )

    fieldId: Optional[str] = Field(
        validation_alias="fieldId", default=None, description="Field ID"
    )

    colName: Optional[str] = Field(
        validation_alias="colName", default=None, description="Column name"
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="Description"
    )

    colType: Optional[str] = Field(
        validation_alias="colType", default=None, description="Column type"
    )

    deviceType: Optional[str] = Field(
        validation_alias="deviceType", default=None, description="Device type"
    )
