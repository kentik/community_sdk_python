# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TenantUser(BaseModel):
    """
    TenantUser
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique system assigned identifier of the user",
    )

    tenantId: str = Field(
        validation_alias="tenantId",
        description="Unique identifier of the tenant the user belongs to",
    )

    userFullName: str = Field(
        validation_alias="userFullName", description="Full name of the user"
    )

    userEmail: str = Field(
        validation_alias="userEmail", description="Email address of the user"
    )
