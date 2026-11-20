# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class RegistrationConfig(BaseModel):
    """
    RegistrationConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    expiresAt: Optional[str] = Field(
        validation_alias="expiresAt",
        default=None,
        description="Time at which the registration becomes invalid (default one hour after creation).",
    )

    allowedPrivateCidrs: Optional[List[str]] = Field(
        validation_alias="allowedPrivateCidrs",
        default=None,
        description="Array of private IP CIDR blocks allowed to register the agent. When not set any IP is allowed\n\nPrivate IP CIDR blocks allowed to register the agent. When empty, any private IP is allowed.",
    )

    allowedPublicCidrs: Optional[List[str]] = Field(
        validation_alias="allowedPublicCidrs",
        default=None,
        description="Array of public IP CIDR blocks allowed to register the agent. When not set any IP is allowed\n\nPublic IP CIDR blocks allowed to register the agent. When empty, any public IP is allowed.",
    )
