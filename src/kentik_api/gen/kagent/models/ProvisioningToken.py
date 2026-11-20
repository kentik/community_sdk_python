# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ProvisioningTokenAgentConfig import ProvisioningTokenAgentConfig
from .TokenRevoked import TokenRevoked


class ProvisioningToken(BaseModel):
    """
    ProvisioningToken
    ProvisioningToken represents a provisioning token for automated agent registration.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    token: Optional[str] = Field(
        validation_alias="token",
        default=None,
        description="Value of the provisioning token (UUID). Treat this value as a credential.",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="User-friendly name of the token.",
    )

    maxUsageCount: Optional[int] = Field(
        validation_alias="maxUsageCount",
        default=None,
        description="Maximum number of agents that can use this token. Defaults to 1\n\nMaximum number of agents that can register with this token (default 1).",
    )

    currentUsageCount: Optional[int] = Field(
        validation_alias="currentUsageCount",
        default=None,
        description="Number of agents already registered with this token.",
    )

    expiresAt: Optional[str] = Field(
        validation_alias="expiresAt",
        default=None,
        description="Time at which the token expires (default one hour after creation).",
    )

    allowedPrivateCidrs: Optional[List[str]] = Field(
        validation_alias="allowedPrivateCidrs",
        default=None,
        description="Array of private IP CIDR blocks allowed to use this token. When not set any IP is allowed\n\nPrivate IP CIDR blocks allowed to use this token. When empty, any private IP is allowed.",
    )

    allowedPublicCidrs: Optional[List[str]] = Field(
        validation_alias="allowedPublicCidrs",
        default=None,
        description="Array of public IP CIDR blocks allowed to use this token. When not set any IP is allowed\n\nPublic IP CIDR blocks allowed to use this token. When empty, any public IP is allowed.",
    )

    clusterId: Optional[str] = Field(
        validation_alias="clusterId",
        default=None,
        description="ID of the cluster to assign agents registered with this token to.",
    )

    requiresApproval: Optional[bool] = Field(
        validation_alias="requiresApproval",
        default=None,
        description="Indication whether agents registered with this token are placed on the pending approval list instead of being approved automatically (default false).",
    )

    config: Optional[ProvisioningTokenAgentConfig] = Field(
        validation_alias="config", default=None
    )

    revoked: Optional[TokenRevoked] = Field(validation_alias="revoked", default=None)

    createdBy: Optional[str] = Field(
        validation_alias="createdBy",
        default=None,
        description="Email of the user who created the token.",
    )

    ctime: Optional[str] = Field(
        validation_alias="ctime", default=None, description="Creation timestamp."
    )

    utime: Optional[str] = Field(
        validation_alias="utime",
        default=None,
        description="Last-modification timestamp.",
    )
