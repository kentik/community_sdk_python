# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class EventPolicySettingsEventType(str, Enum):
    EVENT_TYPE_UNSPECIFIED = "EVENT_TYPE_UNSPECIFIED"

    EVENT_TYPE_SYSLOG = "EVENT_TYPE_SYSLOG"

    EVENT_TYPE_SNMP_TRAP = "EVENT_TYPE_SNMP_TRAP"
