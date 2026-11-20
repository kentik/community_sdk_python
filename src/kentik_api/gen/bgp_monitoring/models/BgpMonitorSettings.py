# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .BgpHealthSettings import BgpHealthSettings
from .Nlri import Nlri


class BgpMonitorSettings(BaseModel):
    """
    BgpMonitorSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    allowedAsns: Optional[List[int]] = Field(
        validation_alias="allowedAsns",
        default=None,
        description="List of ASNs that are valid originators of monitored prefixes",
    )

    targets: List[Nlri] = Field(
        validation_alias="targets", description="List of prefixes to monitor"
    )

    checkRpki: Optional[bool] = Field(
        validation_alias="checkRpki",
        default=None,
        description="Enable verification of validity of advertisements of monitored prefixes with respect to RPKI",
    )

    includeCoveredPrefixes: Optional[bool] = Field(
        validation_alias="includeCoveredPrefixes",
        default=None,
        description="Include advertised subnets (sub-prefixes) of monitored prefixes",
    )

    healthSettings: Optional[BgpHealthSettings] = Field(
        validation_alias="healthSettings", default=None
    )

    notificationChannels: Optional[List[str]] = Field(
        validation_alias="notificationChannels",
        default=None,
        description="List of IDs of notification channels for delivery of alerts",
    )

    notes: Optional[str] = Field(
        validation_alias="notes",
        default=None,
        description="Free form notes documenting the monitor",
    )

    allowedUpstreams: Optional[List[int]] = Field(
        validation_alias="allowedUpstreams",
        default=None,
        description="List of ASNs that are expected to propagate monitored prefixes",
    )
