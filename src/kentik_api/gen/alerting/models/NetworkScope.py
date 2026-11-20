# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class NetworkScope(str, Enum):
    NETWORK_SCOPE_UNSPECIFIED = "NETWORK_SCOPE_UNSPECIFIED"

    NETWORK_SCOPE_ANY = "NETWORK_SCOPE_ANY"

    NETWORK_SCOPE_ROOT = "NETWORK_SCOPE_ROOT"

    NETWORK_SCOPE_SOURCE = "NETWORK_SCOPE_SOURCE"

    NETWORK_SCOPE_DESTINATION = "NETWORK_SCOPE_DESTINATION"

    NETWORK_SCOPE_ADJACENT = "NETWORK_SCOPE_ADJACENT"
