# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CredentialType import CredentialType
from .Token import Token


class CredentialServiceUpdateCredentialGroupBody(BaseModel):
    """
    UpdateCredentialGroupRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    type: CredentialType = Field(validation_alias="type")

    description: Optional[str] = Field(validation_alias="description", default=None)

    tokens: List[Token] = Field(validation_alias="tokens")

    labels: Optional[List[str]] = Field(
        validation_alias="labels", default=None, description="Label ids"
    )
