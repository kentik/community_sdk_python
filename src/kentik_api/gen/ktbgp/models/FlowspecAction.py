# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowspecActionAccept import FlowspecActionAccept
from .FlowspecActionDiscard import FlowspecActionDiscard
from .FlowspecActionExtendedCommunity import FlowspecActionExtendedCommunity
from .FlowspecActionIPNextHopCopy import FlowspecActionIPNextHopCopy
from .FlowspecActionIPNextHopRedirect import FlowspecActionIPNextHopRedirect
from .FlowspecActionLargeCommunity import FlowspecActionLargeCommunity
from .FlowspecActionMarkDSCP import FlowspecActionMarkDSCP
from .FlowspecActionRegularCommunity import FlowspecActionRegularCommunity
from .FlowspecActionRouteTargetRedirect import FlowspecActionRouteTargetRedirect
from .FlowspecActionTerminalSample import FlowspecActionTerminalSample
from .FlowspecActionTrafficRateBytes import FlowspecActionTrafficRateBytes


class FlowspecAction(BaseModel):
    """
    FlowspecAction model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    accept: Optional[FlowspecActionAccept] = Field(
        validation_alias="accept", default=None
    )

    discard: Optional[FlowspecActionDiscard] = Field(
        validation_alias="discard", default=None
    )

    rateBytes: Optional[FlowspecActionTrafficRateBytes] = Field(
        validation_alias="rateBytes", default=None
    )

    markDscp: Optional[FlowspecActionMarkDSCP] = Field(
        validation_alias="markDscp", default=None
    )

    rtRedirect: Optional[FlowspecActionRouteTargetRedirect] = Field(
        validation_alias="rtRedirect", default=None
    )

    ipRedirect: Optional[FlowspecActionIPNextHopRedirect] = Field(
        validation_alias="ipRedirect", default=None
    )

    actionType: Optional[FlowspecActionTerminalSample] = Field(
        validation_alias="actionType", default=None
    )

    rtCopy: Optional[FlowspecActionIPNextHopCopy] = Field(
        validation_alias="rtCopy", default=None
    )

    regularCommunity: Optional[FlowspecActionRegularCommunity] = Field(
        validation_alias="regularCommunity", default=None
    )

    extendedCommunity: Optional[FlowspecActionExtendedCommunity] = Field(
        validation_alias="extendedCommunity", default=None
    )

    largeCommunity: Optional[FlowspecActionLargeCommunity] = Field(
        validation_alias="largeCommunity", default=None
    )
