# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TenantUser import TenantUser


class ListTenantUserResponse(BaseModel):
    """
    ListTenantUserResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    users: Optional[List[Optional[TenantUser]]] = Field(
        validation_alias="users", default=None
    )

    invalidCount: Optional[int] = Field(validation_alias="invalidCount", default=None)
