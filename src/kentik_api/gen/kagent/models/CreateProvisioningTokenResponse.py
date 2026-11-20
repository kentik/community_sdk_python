# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ProvisioningToken import ProvisioningToken


class CreateProvisioningTokenResponse(BaseModel):
    """
    CreateProvisioningTokenResponse
    Response message for creating a provisioning token.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    token: Optional[ProvisioningToken] = Field(validation_alias="token", default=None)
