# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class Usage(str, Enum):
    USAGE_UNSPECIFIED = "USAGE_UNSPECIFIED"

    USAGE_QUERY = "USAGE_QUERY"

    USAGE_KMETRICS_ALERT = "USAGE_KMETRICS_ALERT"

    USAGE_FLOW_ALERT = "USAGE_FLOW_ALERT"
