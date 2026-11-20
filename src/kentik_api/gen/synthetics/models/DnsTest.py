# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .DNSRecord import DNSRecord


class DnsTest(BaseModel):
    """
    DnsTest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target",
        default=None,
        description="Fully qualified DNS name to query",
    )

    timeout: Optional[int] = Field(
        validation_alias="timeout",
        default=None,
        description="--- Deprecated: value is ignored. ---",
    )

    recordType: Optional[DNSRecord] = Field(validation_alias="recordType", default=None)

    servers: Optional[List[str]] = Field(
        validation_alias="servers",
        default=None,
        description="List of IP addresses of DNS servers",
    )

    port: Optional[int] = Field(
        validation_alias="port", default=None, description="Target DNS server port"
    )
