# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TestPingSettings(BaseModel):
    """
    TestPingSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    count: Optional[int] = Field(
        validation_alias="count",
        default=None,
        description="Number of probe packets to send in one iteration",
    )

    protocol: Optional[str] = Field(
        validation_alias="protocol",
        default=None,
        description="Transport protocol to use (icmp | tcp)",
    )

    port: Optional[int] = Field(
        validation_alias="port",
        default=None,
        description="Target port for TCP probes (ignored for ICMP)",
    )

    timeout: Optional[int] = Field(
        validation_alias="timeout",
        default=None,
        description="Timeout in milliseconds for execution of the task",
    )

    delay: Optional[float] = Field(
        validation_alias="delay",
        default=None,
        description="Inter-probe delay in milliseconds",
    )

    dscp: Optional[int] = Field(
        validation_alias="dscp",
        default=None,
        description="DSCP code to be set in IP header of probe packets",
    )
