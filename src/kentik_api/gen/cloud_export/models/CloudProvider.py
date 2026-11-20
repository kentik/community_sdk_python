# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class CloudProvider(str, Enum):
    CLOUD_PROVIDER_UNSPECIFIED = "CLOUD_PROVIDER_UNSPECIFIED"

    CLOUD_PROVIDER_AWS = "CLOUD_PROVIDER_AWS"

    CLOUD_PROVIDER_AZURE = "CLOUD_PROVIDER_AZURE"

    CLOUD_PROVIDER_GCE = "CLOUD_PROVIDER_GCE"

    CLOUD_PROVIDER_OCI = "CLOUD_PROVIDER_OCI"
