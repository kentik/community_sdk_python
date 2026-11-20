# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class InstallerType(str, Enum):
    INSTALLER_TYPE_UNSPECIFIED = "INSTALLER_TYPE_UNSPECIFIED"

    INSTALLER_TYPE_LINUX = "INSTALLER_TYPE_LINUX"

    INSTALLER_TYPE_DOCKER = "INSTALLER_TYPE_DOCKER"

    INSTALLER_TYPE_RPM = "INSTALLER_TYPE_RPM"

    INSTALLER_TYPE_DEB = "INSTALLER_TYPE_DEB"
