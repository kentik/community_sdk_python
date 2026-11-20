# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class Role(str, Enum):
    ROLE_UNSPECIFIED = "ROLE_UNSPECIFIED"

    ROLE_MEMBER = "ROLE_MEMBER"

    ROLE_ADMINISTRATOR = "ROLE_ADMINISTRATOR"

    ROLE_SUPER_ADMINISTRATOR = "ROLE_SUPER_ADMINISTRATOR"
