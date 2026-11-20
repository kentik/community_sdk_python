# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class ReleaseSource(str, Enum):
    RELEASE_SOURCE_UNSPECIFIED = "RELEASE_SOURCE_UNSPECIFIED"

    RELEASE_SOURCE_MANAGED = "RELEASE_SOURCE_MANAGED"

    RELEASE_SOURCE_LOCAL = "RELEASE_SOURCE_LOCAL"
