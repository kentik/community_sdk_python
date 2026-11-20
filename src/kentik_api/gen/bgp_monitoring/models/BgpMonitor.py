# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BgpMonitorSettings import BgpMonitorSettings
from .BgpMonitorStatus import BgpMonitorStatus
from .UserInfo import UserInfo


class BgpMonitor(BaseModel):
    """
    BgpMonitor
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="System generated unique identifier",
    )

    name: str = Field(
        validation_alias="name", description="User selected name of the monitor"
    )

    status: Optional[BgpMonitorStatus] = Field(validation_alias="status", default=None)

    settings: Optional[BgpMonitorSettings] = Field(
        validation_alias="settings", default=None
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    createdBy: Optional[UserInfo] = Field(validation_alias="createdBy", default=None)

    lastUpdatedBy: Optional[UserInfo] = Field(
        validation_alias="lastUpdatedBy", default=None
    )

    labels: Optional[List[str]] = Field(validation_alias="labels", default=None)
