# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class TenantUserServiceCreateTenantUserBody(BaseModel):
    """
    CreateTenantUserRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    user: Optional[Dict[str, Any]] = Field(
        validation_alias="user", default=None, description="TenantUser"
    )
