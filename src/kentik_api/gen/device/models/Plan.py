# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Plan(BaseModel):
    """
    Plan
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="Plan ID"
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Plan name"
    )

    active: Optional[bool] = Field(
        validation_alias="active", default=None, description="Plan Status"
    )

    bgp: Optional[bool] = Field(
        validation_alias="bgp", default=None, description="BGP enabled"
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId", default=None, description="Company ID"
    )

    description: Optional[str] = Field(
        validation_alias="description", default=None, description="Plan Description"
    )

    deviceTypes: Optional[List[str]] = Field(
        validation_alias="deviceTypes", default=None, description="Device Types"
    )

    devices: Optional[List[str]] = Field(
        validation_alias="devices", default=None, description="Devices"
    )

    fastRetention: Optional[int] = Field(
        validation_alias="fastRetention",
        default=None,
        description="Fast Rention in days",
    )

    fullRetention: Optional[int] = Field(
        validation_alias="fullRetention",
        default=None,
        description="Full Retention in days",
    )

    maxBigdataFps: Optional[int] = Field(
        validation_alias="maxBigdataFps", default=None, description="Max data FPS"
    )

    maxDevices: Optional[int] = Field(
        validation_alias="maxDevices", default=None, description="Max Device"
    )

    maxFps: Optional[int] = Field(
        validation_alias="maxFps", default=None, description="Max FPS"
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Created Date"
    )

    edate: Optional[str] = Field(
        validation_alias="edate", default=None, description="Updated Data"
    )

    metadata: Optional[Dict[str, Any]] = Field(
        validation_alias="metadata", default=None, description="Plan Metadata"
    )
