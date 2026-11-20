# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class FieldBy(str, Enum):
    BY_UNSPECIFIED = "BY_UNSPECIFIED"

    BY_ID = "BY_ID"

    BY_NAME = "BY_NAME"

    BY_CREATED_AT = "BY_CREATED_AT"

    BY_UPDATED_AT = "BY_UPDATED_AT"

    BY_SEVERITY = "BY_SEVERITY"

    BY_STATUS = "BY_STATUS"

    BY_POLICY_TYPE = "BY_POLICY_TYPE"

    BY_START_TIME = "BY_START_TIME"

    BY_END_TIME = "BY_END_TIME"

    BY_ALARM_STATE = "BY_ALARM_STATE"

    BY_ALARM_POLICY_NAME = "BY_ALARM_POLICY_NAME"

    BY_ALARM_PRIMARY_DIMENSION = "BY_ALARM_PRIMARY_DIMENSION"
