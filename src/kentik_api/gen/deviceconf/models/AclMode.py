# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class AclMode(str, Enum):
    ACL_MODE_UNSPECIFIED = "ACL_MODE_UNSPECIFIED"

    ACL_MODE_EXACT = "ACL_MODE_EXACT"

    ACL_MODE_CONTAINS = "ACL_MODE_CONTAINS"

    ACL_MODE_REGEX = "ACL_MODE_REGEX"
