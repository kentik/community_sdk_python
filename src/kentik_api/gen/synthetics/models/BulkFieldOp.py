# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class BulkFieldOp(str, Enum):
    BULK_FIELD_OP_UNSPECIFIED = "BULK_FIELD_OP_UNSPECIFIED"

    BULK_FIELD_OP_REPLACE = "BULK_FIELD_OP_REPLACE"

    BULK_FIELD_OP_ADD = "BULK_FIELD_OP_ADD"

    BULK_FIELD_OP_REMOVE = "BULK_FIELD_OP_REMOVE"
