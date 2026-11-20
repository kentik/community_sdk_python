# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .TenantUser import TenantUser


class UpdateTenantUserResponse(BaseModel):
    """
    UpdateTenantUserResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    user: Optional[TenantUser] = Field(validation_alias="user", default=None)
