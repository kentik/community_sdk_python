# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .FlowspecUpdate import FlowspecUpdate
from .RTBHUpdate import RTBHUpdate


class DeviceAdverts(BaseModel):
    """
    DeviceAdverts model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceId: Optional[str] = Field(validation_alias="deviceId", default=None)

    flowspec: Optional[List[Optional[FlowspecUpdate]]] = Field(
        validation_alias="flowspec", default=None
    )

    rtbh: Optional[List[Optional[RTBHUpdate]]] = Field(
        validation_alias="rtbh", default=None
    )
