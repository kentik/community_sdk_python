# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CredentialGroup import CredentialGroup


class ListCredentialGroupResponse(BaseModel):
    """
    ListCredentialGroupsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    groups: Optional[List[Optional[CredentialGroup]]] = Field(
        validation_alias="groups", default=None
    )
