# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Label(BaseModel):
    """
    Label
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="Label ID"
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Label name"
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="Label description"
    )

    edate: Optional[str] = Field(
        validation_alias="edate", default=None, description="Label end date (UTC)"
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Label creation date (UTC)"
    )

    userId: Optional[str] = Field(
        validation_alias="userId", default=None, description="User ID"
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId", default=None, description="Company ID"
    )

    color: Optional[str] = Field(
        validation_alias="color", default=None, description="Label color"
    )

    order: Optional[str] = Field(
        validation_alias="order", default=None, description="Label order"
    )

    pivotDeviceId: Optional[str] = Field(
        validation_alias="pivotDeviceId", default=None, description="Pivot device ID"
    )

    pivotLabelId: Optional[str] = Field(
        validation_alias="pivotLabelId", default=None, description="Pivot label ID"
    )
