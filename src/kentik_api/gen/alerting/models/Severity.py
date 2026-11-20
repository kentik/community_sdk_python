# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class Severity(str, Enum):
    SEVERITY_UNSPECIFIED = "SEVERITY_UNSPECIFIED"

    SEVERITY_CLEAR = "SEVERITY_CLEAR"

    SEVERITY_MINOR = "SEVERITY_MINOR"

    SEVERITY_WARNING = "SEVERITY_WARNING"

    SEVERITY_MAJOR = "SEVERITY_MAJOR"

    SEVERITY_SEVERE = "SEVERITY_SEVERE"

    SEVERITY_CRITICAL = "SEVERITY_CRITICAL"
