# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BundleSource import BundleSource
from .ConfigSource import ConfigSource
from .HostMetadata import HostMetadata
from .InstallerType import InstallerType
from .ReleaseSource import ReleaseSource


class InstallConfig(BaseModel):
    """
    InstallConfig
    Describes an individual agent install configuration
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier of the install.",
    )

    type: Optional[InstallerType] = Field(validation_alias="type", default=None)

    hostMetadata: Optional[HostMetadata] = Field(
        validation_alias="hostMetadata", default=None
    )

    releaseSource: Optional[ReleaseSource] = Field(
        validation_alias="releaseSource", default=None
    )

    configSource: Optional[ConfigSource] = Field(
        validation_alias="configSource", default=None
    )

    bundleSource: Optional[BundleSource] = Field(
        validation_alias="bundleSource", default=None
    )
