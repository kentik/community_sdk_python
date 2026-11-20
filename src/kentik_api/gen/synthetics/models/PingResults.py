# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .MetricData import MetricData
from .PacketLossData import PacketLossData


class PingResults(BaseModel):
    """
    PingResults
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target",
        default=None,
        description="Hostname or address of the probed target",
    )

    packetLoss: Optional[PacketLossData] = Field(
        validation_alias="packetLoss", default=None
    )

    latency: Optional[MetricData] = Field(validation_alias="latency", default=None)

    jitter: Optional[MetricData] = Field(validation_alias="jitter", default=None)

    dstIp: Optional[str] = Field(
        validation_alias="dstIp",
        default=None,
        description="IP address of probed target",
    )
