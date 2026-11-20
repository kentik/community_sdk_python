# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .FlowContextDeviceDetails import FlowContextDeviceDetails
from .FlowContextInterfaceDetails import FlowContextInterfaceDetails
from .FlowContextSiteDetails import FlowContextSiteDetails


class FlowContextAlertKeyDetails(BaseModel):
    """
    FlowContextAlertKeyDetails model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    device: Optional[FlowContextDeviceDetails] = Field(
        validation_alias="device", default=None
    )

    interface: Optional[FlowContextInterfaceDetails] = Field(
        validation_alias="interface", default=None
    )

    site: Optional[FlowContextSiteDetails] = Field(
        validation_alias="site", default=None
    )

    extendedValue: Optional[str] = Field(
        validation_alias="extendedValue",
        default=None,
        description="The extended value of the alert key.",
    )
