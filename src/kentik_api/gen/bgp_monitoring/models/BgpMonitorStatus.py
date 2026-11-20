# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class BgpMonitorStatus(str, Enum):
    BGP_MONITOR_STATUS_UNSPECIFIED = "BGP_MONITOR_STATUS_UNSPECIFIED"

    BGP_MONITOR_STATUS_ACTIVE = "BGP_MONITOR_STATUS_ACTIVE"

    BGP_MONITOR_STATUS_PAUSED = "BGP_MONITOR_STATUS_PAUSED"

    BGP_MONITOR_STATUS_DELETED = "BGP_MONITOR_STATUS_DELETED"
