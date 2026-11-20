# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class SiteType(str, Enum):
    SITE_TYPE_UNSPECIFIED = "SITE_TYPE_UNSPECIFIED"

    SITE_TYPE_DATA_CENTER = "SITE_TYPE_DATA_CENTER"

    SITE_TYPE_CLOUD = "SITE_TYPE_CLOUD"

    SITE_TYPE_BRANCH = "SITE_TYPE_BRANCH"

    SITE_TYPE_CONNECTIVITY = "SITE_TYPE_CONNECTIVITY"

    SITE_TYPE_CUSTOMER = "SITE_TYPE_CUSTOMER"

    SITE_TYPE_OTHER = "SITE_TYPE_OTHER"
