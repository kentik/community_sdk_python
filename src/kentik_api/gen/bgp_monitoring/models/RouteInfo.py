# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Nlri import Nlri
from .RpkiStatus import RpkiStatus
from .VantagePoint import VantagePoint


class RouteInfo(BaseModel):
    """
    RouteInfo
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    nlri: Optional[Nlri] = Field(validation_alias="nlri", default=None)

    originAsn: Optional[int] = Field(
        validation_alias="originAsn",
        default=None,
        description="The autonomous system number originating the NLRI",
    )

    asPath: Optional[List[str]] = Field(
        validation_alias="asPath",
        default=None,
        description="AS path observed at the vantage point for the NLRI",
    )

    vantagePoint: Optional[VantagePoint] = Field(
        validation_alias="vantagePoint", default=None
    )

    rpkiStatus: Optional[RpkiStatus] = Field(
        validation_alias="rpkiStatus", default=None
    )

    nexthop: Optional[str] = Field(
        validation_alias="nexthop",
        default=None,
        description="IP address of the first route hop from the vantage point toward the target",
    )
