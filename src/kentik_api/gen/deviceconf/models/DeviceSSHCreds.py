# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DeviceSSHCreds(BaseModel):
    """
    DeviceSSHCreds model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    username: Optional[str] = Field(validation_alias="username", default=None)

    privateKey: Optional[str] = Field(validation_alias="privateKey", default=None)

    passphrase: Optional[str] = Field(
        validation_alias="passphrase",
        default=None,
        description="used as password if private_key is empty",
    )
