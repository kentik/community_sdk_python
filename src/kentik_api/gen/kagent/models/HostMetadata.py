# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class HostMetadata(BaseModel):
    """
    HostMetadata
    Read-only metadata about a host system
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    hostname: Optional[str] = Field(
        validation_alias="hostname",
        default=None,
        description="Hostname of the host the agent runs on.",
    )

    machineId: Optional[str] = Field(
        validation_alias="machineId",
        default=None,
        description="Machine identifier of the host the agent runs on.",
    )

    publicIp: Optional[str] = Field(
        validation_alias="publicIp",
        default=None,
        description="Public IP address of the host the agent runs on.",
    )

    privateIp: Optional[str] = Field(
        validation_alias="privateIp",
        default=None,
        description="Private IP address of the host the agent runs on.",
    )

    os: Optional[str] = Field(
        validation_alias="os",
        default=None,
        description="linux,darwin,windows\n\nOperating system of the host. One of `linux`, `darwin` or `windows`.",
    )

    arch: Optional[str] = Field(
        validation_alias="arch",
        default=None,
        description="amd64,arm64\n\nCPU architecture of the host, for example `amd64` or `arm64`.",
    )
