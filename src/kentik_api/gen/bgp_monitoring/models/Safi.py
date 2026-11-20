# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class Safi(str, Enum):
    SAFI_UNSPECIFIED = "SAFI_UNSPECIFIED"

    SAFI_UNICAST = "SAFI_UNICAST"

    SAFI_MPLS = "SAFI_MPLS"

    SAFI_L3VPN = "SAFI_L3VPN"
