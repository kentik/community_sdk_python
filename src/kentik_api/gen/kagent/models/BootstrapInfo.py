# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class BootstrapInfo(BaseModel):
    """
    BootstrapInfo
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    linuxInstallCommand: Optional[str] = Field(
        validation_alias="linuxInstallCommand",
        default=None,
        description="curl command to install the agent on linux\n\nCommand installing the agent directly on a Linux host. Contains a provisioning token.",
    )

    dockerInstallCommand: Optional[str] = Field(
        validation_alias="dockerInstallCommand",
        default=None,
        description="docker command to install the agent in docker\n\nCommand installing the agent as a Docker container. Contains a provisioning token.",
    )

    provisioningToken: Optional[str] = Field(
        validation_alias="provisioningToken",
        default=None,
        description="provisioning token to use in the install commands; treat as a credential\n\nProvisioning token embedded in the install commands. Treat this value as a credential.",
    )
