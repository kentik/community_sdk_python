# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CompatibilityInfo import CompatibilityInfo


class CapabilityRelease(BaseModel):
    """
    CapabilityRelease
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    capability: Optional[str] = Field(
        validation_alias="capability",
        default=None,
        description="The capability name: one of kagent, kproxy, ranger and so on.",
    )

    semver: Optional[str] = Field(
        validation_alias="semver", default=None, description="The semantic version."
    )

    downloadUrls: Optional[List[str]] = Field(
        validation_alias="downloadUrls",
        default=None,
        description="A list of accepted URLs to download the capability",
    )

    checksum: Optional[str] = Field(
        validation_alias="checksum",
        default=None,
        description="deprecated, use provenance field instead\n\nThe hex-encoded checksum",
    )

    checksumAlgorithm: Optional[str] = Field(
        validation_alias="checksumAlgorithm",
        default=None,
        description="deprecated, use provenance field instead\n\nThe checksum algorithm: one of sha256, md5, and so on...",
    )

    provenance: Optional[str] = Field(
        validation_alias="provenance",
        default=None,
        description="Provenance data in intoto format",
    )

    supportedDistros: Optional[List[str]] = Field(
        validation_alias="supportedDistros",
        default=None,
        description="The list of supported distributions for this release. Only applicable for capabilities that generate distro specific binaries, such as kproxy. ",
    )

    compatibility: Optional[CompatibilityInfo] = Field(
        validation_alias="compatibility", default=None
    )
