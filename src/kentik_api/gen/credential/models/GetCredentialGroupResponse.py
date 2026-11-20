# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CredentialGroup import CredentialGroup


class GetCredentialGroupResponse(BaseModel):
    """
    GetCredentialGroupResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    group: Optional[CredentialGroup] = Field(validation_alias="group", default=None)
