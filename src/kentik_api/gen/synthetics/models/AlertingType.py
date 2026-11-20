# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class AlertingType(str, Enum):
    ALERTING_TYPE_UNSPECIFIED = "ALERTING_TYPE_UNSPECIFIED"

    ALERTING_TYPE_AGENT = "ALERTING_TYPE_AGENT"

    ALERTING_TYPE_GROUPED = "ALERTING_TYPE_GROUPED"

    ALERTING_TYPE_SUBTEST = "ALERTING_TYPE_SUBTEST"
