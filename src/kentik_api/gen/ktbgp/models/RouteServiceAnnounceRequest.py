# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FlowspecUpdate import FlowspecUpdate
from .RTBHUpdate import RTBHUpdate


class RouteServiceAnnounceRequest(BaseModel):
    """
    RouteServiceAnnounceRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceIds: Optional[List[str]] = Field(validation_alias="deviceIds", default=None)

    flowspec: Optional[FlowspecUpdate] = Field(
        validation_alias="flowspec", default=None
    )

    rtbh: Optional[RTBHUpdate] = Field(validation_alias="rtbh", default=None)
