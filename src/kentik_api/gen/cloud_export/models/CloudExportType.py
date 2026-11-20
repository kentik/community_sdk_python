# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class CloudExportType(str, Enum):
    CLOUD_EXPORT_TYPE_UNSPECIFIED = "CLOUD_EXPORT_TYPE_UNSPECIFIED"

    CLOUD_EXPORT_TYPE_KENTIK_MANAGED = "CLOUD_EXPORT_TYPE_KENTIK_MANAGED"

    CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED = "CLOUD_EXPORT_TYPE_CUSTOMER_MANAGED"
