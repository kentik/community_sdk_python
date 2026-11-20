# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ProvisioningToken import ProvisioningToken


class ListProvisioningTokensResponse(BaseModel):
    """
    ListProvisioningTokensResponse
    Response message for listing provisioning tokens.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tokens: Optional[List[Optional[ProvisioningToken]]] = Field(
        validation_alias="tokens",
        default=None,
        description="List of provisioning token objects.",
    )
