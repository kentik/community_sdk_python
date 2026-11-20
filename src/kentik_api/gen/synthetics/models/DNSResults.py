# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .DNSResponseData import DNSResponseData
from .MetricData import MetricData


class DNSResults(BaseModel):
    """
    DNSResults
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target", default=None, description="Queried DNS record"
    )

    server: Optional[str] = Field(
        validation_alias="server",
        default=None,
        description="DNS server used for the query",
    )

    latency: Optional[MetricData] = Field(validation_alias="latency", default=None)

    response: Optional[DNSResponseData] = Field(
        validation_alias="response", default=None
    )
