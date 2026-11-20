# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from enum import Enum


class DNSRecord(str, Enum):
    DNS_RECORD_UNSPECIFIED = "DNS_RECORD_UNSPECIFIED"

    DNS_RECORD_A = "DNS_RECORD_A"

    DNS_RECORD_AAAA = "DNS_RECORD_AAAA"

    DNS_RECORD_CNAME = "DNS_RECORD_CNAME"

    DNS_RECORD_DNAME = "DNS_RECORD_DNAME"

    DNS_RECORD_NS = "DNS_RECORD_NS"

    DNS_RECORD_MX = "DNS_RECORD_MX"

    DNS_RECORD_PTR = "DNS_RECORD_PTR"

    DNS_RECORD_SOA = "DNS_RECORD_SOA"
