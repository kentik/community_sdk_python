# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .DeviceSubtype import DeviceSubtype
from .PlanDevice import PlanDevice


class Plan(BaseModel):
    """
    Represents a plan object.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="The system-assigned unique ID of the plan.",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId",
        default=None,
        description="The system-assigned unique ID of your organization.",
    )

    name: str = Field(
        validation_alias="name",
        description='A name for the plan. Every Kentik customer is initially provided with a plan called "Default."',
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="An optional description of the plan.",
    )

    active: Optional[bool] = Field(
        validation_alias="active",
        default=None,
        description="Indicates if the plan is currently activated.",
    )

    maxDevices: Optional[int] = Field(
        validation_alias="maxDevices",
        default=None,
        description="The maximum number of devices that can send flow records to Kentik under this plan.",
    )

    maxFps: Optional[int] = Field(
        validation_alias="maxFps",
        default=None,
        description="Per device limit on flow records per second that can be sent to Kentik (excess FPS may trigger rate-limiting).",
    )

    bgpEnabled: Optional[bool] = Field(
        validation_alias="bgpEnabled",
        default=None,
        description="Indicates whether or not devices on this plan may be peered to enable Kentik to collect BGP routing data.",
    )

    fastRetention: Optional[int] = Field(
        validation_alias="fastRetention",
        default=None,
        description="The number of days that data will be stored in the Fast dataseries.",
    )

    fullRetention: Optional[int] = Field(
        validation_alias="fullRetention",
        default=None,
        description="The number of days that data will be stored in the Full dataseries.",
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="The system-assigned date-time of filter creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="The system-assigned date-time of most-recent modification, in UTC.",
    )

    maxBigdataFps: Optional[int] = Field(
        validation_alias="maxBigdataFps",
        default=None,
        description="Max FPS applied to fast data rollups.",
    )

    deviceTypes: Optional[List[Optional[DeviceSubtype]]] = Field(
        validation_alias="deviceTypes",
        default=None,
        description="The types of allowed devices.",
    )

    devices: Optional[List[Optional[PlanDevice]]] = Field(
        validation_alias="devices",
        default=None,
        description="The devices currently assigned to this plan.",
    )

    metadata: Optional[Dict[str, Any]] = Field(
        validation_alias="metadata",
        default=None,
        description="Additional custom metadata associated with the plan.",
    )
