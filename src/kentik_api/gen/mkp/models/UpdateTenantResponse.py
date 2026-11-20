# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Tenant import Tenant


class UpdateTenantResponse(BaseModel):
    """
    UpdateTenantResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tenant: Optional[Tenant] = Field(validation_alias="tenant", default=None)
