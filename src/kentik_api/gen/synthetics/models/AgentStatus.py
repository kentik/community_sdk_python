# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class AgentStatus(str, Enum):
    AGENT_STATUS_UNSPECIFIED = "AGENT_STATUS_UNSPECIFIED"

    AGENT_STATUS_OK = "AGENT_STATUS_OK"

    AGENT_STATUS_WAIT = "AGENT_STATUS_WAIT"

    AGENT_STATUS_DELETED = "AGENT_STATUS_DELETED"
