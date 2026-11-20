# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .InterfacesDetailStatusDetail import InterfacesDetailStatusDetail


class CapacitySummaryInterfacesDetail(BaseModel):
    """
    InterfacesDetail
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    totalCount: Optional[int] = Field(
        validation_alias="totalCount",
        default=None,
        description="Total number of interfaces",
    )

    totalCapacityBps: Optional[str] = Field(
        validation_alias="totalCapacityBps",
        default=None,
        description="Total capacity in bps",
    )

    healthy: Optional[InterfacesDetailStatusDetail] = Field(
        validation_alias="healthy", default=None
    )

    warning: Optional[InterfacesDetailStatusDetail] = Field(
        validation_alias="warning", default=None
    )

    critical: Optional[InterfacesDetailStatusDetail] = Field(
        validation_alias="critical", default=None
    )
