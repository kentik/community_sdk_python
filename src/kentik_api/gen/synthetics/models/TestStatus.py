# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class TestStatus(str, Enum):
    TEST_STATUS_UNSPECIFIED = "TEST_STATUS_UNSPECIFIED"

    TEST_STATUS_ACTIVE = "TEST_STATUS_ACTIVE"

    TEST_STATUS_PAUSED = "TEST_STATUS_PAUSED"

    TEST_STATUS_DELETED = "TEST_STATUS_DELETED"

    TEST_STATUS_PREVIEW = "TEST_STATUS_PREVIEW"
