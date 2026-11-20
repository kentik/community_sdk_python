# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CapacityPlanInterfaceDetail(BaseModel):
    """
    InterfaceDetail
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceName: Optional[str] = Field(
        validation_alias="deviceName", default=None, description="Device name"
    )

    intfName: Optional[str] = Field(
        validation_alias="intfName", default=None, description="Interface name"
    )

    intfDescription: Optional[str] = Field(
        validation_alias="intfDescription",
        default=None,
        description="Interface description",
    )

    intfCapacity: Optional[str] = Field(
        validation_alias="intfCapacity", default=None, description="Interface capacity"
    )

    networkBoundary: Optional[str] = Field(
        validation_alias="networkBoundary", default=None, description="Network boundary"
    )

    connType: Optional[str] = Field(
        validation_alias="connType", default=None, description="Connectivity type"
    )

    provider: Optional[str] = Field(
        validation_alias="provider", default=None, description="Provider"
    )

    utilStatus: Optional[str] = Field(
        validation_alias="utilStatus", default=None, description="Utilization status"
    )

    utilOutMbps: Optional[str] = Field(
        validation_alias="utilOutMbps", default=None, description="Utilization out mbps"
    )

    utilOutPct: Optional[str] = Field(
        validation_alias="utilOutPct",
        default=None,
        description="Utilization out percentage",
    )

    utilInMbps: Optional[str] = Field(
        validation_alias="utilInMbps", default=None, description="Utilization in mbps"
    )

    utilInPct: Optional[str] = Field(
        validation_alias="utilInPct",
        default=None,
        description="Utilization in percentage",
    )

    runoutStatus: Optional[str] = Field(
        validation_alias="runoutStatus", default=None, description="Runout status"
    )

    runoutInDate: Optional[str] = Field(
        validation_alias="runoutInDate", default=None, description="Runout in date"
    )

    runoutInVariation: Optional[str] = Field(
        validation_alias="runoutInVariation",
        default=None,
        description="Runout in variation",
    )

    runoutOutDate: Optional[str] = Field(
        validation_alias="runoutOutDate", default=None, description="Runout out date"
    )

    runoutOutVariation: Optional[str] = Field(
        validation_alias="runoutOutVariation",
        default=None,
        description="Runout out variation",
    )
