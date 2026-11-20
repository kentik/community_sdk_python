# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DevicePlatform import DevicePlatform
from .DeviceSSHCreds import DeviceSSHCreds
from .FetchParameters import FetchParameters


class Device(BaseModel):
    """
    Device model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(validation_alias="id", default=None)

    name: Optional[str] = Field(validation_alias="name", default=None)

    hostname: Optional[str] = Field(
        validation_alias="hostname", default=None, description="or IP address"
    )

    platform: Optional[DevicePlatform] = Field(
        validation_alias="platform", default=None
    )

    sshCreds: Optional[DeviceSSHCreds] = Field(
        validation_alias="sshCreds", default=None
    )

    fetchParams: Optional[FetchParameters] = Field(
        validation_alias="fetchParams", default=None
    )
