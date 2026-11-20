# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .RuntimeConfigEnvVar import RuntimeConfigEnvVar


class RuntimeConfig(BaseModel):
    """
    RuntimeConfig
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    args: Optional[List[str]] = Field(
        validation_alias="args",
        default=None,
        description="command arguments\n\nCommand arguments passed to the process.",
    )

    env: Optional[List[Optional[RuntimeConfigEnvVar]]] = Field(
        validation_alias="env",
        default=None,
        description="environment variables\n\nEnvironment variables set for the process.",
    )

    binary: Optional[str] = Field(
        validation_alias="binary",
        default=None,
        description="binary name\n\nName of the binary to run.",
    )

    linuxCapabilities: Optional[List[str]] = Field(
        validation_alias="linuxCapabilities",
        default=None,
        description="linux capabilities that should be added to the process\n\nLinux capabilities added to the process.",
    )
