# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class EntityType(str, Enum):
    ENTITY_TYPE_UNSPECIFIED = "ENTITY_TYPE_UNSPECIFIED"

    ENTITY_TYPE_SUBNET = "ENTITY_TYPE_SUBNET"

    ENTITY_TYPE_INSTANCE = "ENTITY_TYPE_INSTANCE"

    ENTITY_TYPE_NETWORK_INTERFACE = "ENTITY_TYPE_NETWORK_INTERFACE"
