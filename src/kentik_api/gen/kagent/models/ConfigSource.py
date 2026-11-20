# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class ConfigSource(str, Enum):
    CONFIG_SOURCE_UNSPECIFIED = "CONFIG_SOURCE_UNSPECIFIED"

    CONFIG_SOURCE_MANAGED = "CONFIG_SOURCE_MANAGED"

    CONFIG_SOURCE_LOCAL = "CONFIG_SOURCE_LOCAL"
