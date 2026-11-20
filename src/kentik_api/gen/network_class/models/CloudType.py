# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class CloudType(str, Enum):
    CLOUD_TYPE_UNSPECIFIED = "CLOUD_TYPE_UNSPECIFIED"

    CLOUD_TYPE_AWS = "CLOUD_TYPE_AWS"

    CLOUD_TYPE_AZURE = "CLOUD_TYPE_AZURE"

    CLOUD_TYPE_GCE = "CLOUD_TYPE_GCE"

    CLOUD_TYPE_IBM = "CLOUD_TYPE_IBM"
