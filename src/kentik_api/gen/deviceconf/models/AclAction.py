# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class AclAction(str, Enum):
    ACL_ACTION_UNSPECIFIED = "ACL_ACTION_UNSPECIFIED"

    ACL_ACTION_ALLOW = "ACL_ACTION_ALLOW"

    ACL_ACTION_DENY = "ACL_ACTION_DENY"
