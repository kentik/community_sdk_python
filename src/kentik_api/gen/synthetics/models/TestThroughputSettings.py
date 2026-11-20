# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class TestThroughputSettings(BaseModel):
    """
    TestThroughputSettings
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    port: Optional[int] = Field(
        validation_alias="port",
        default=None,
        description="Target port for TCP or UDP throughput task (the port the target server is listening on)",
    )

    omit: Optional[int] = Field(
        validation_alias="omit",
        default=None,
        description="(optional) Number of seconds to omit from the start of the test",
    )

    duration: Optional[int] = Field(
        validation_alias="duration",
        default=None,
        description="Duration of the test in seconds",
    )

    bandwidth: Optional[int] = Field(
        validation_alias="bandwidth",
        default=None,
        description="(optional) Target bandwidth in Mbps, if no bandwidth is specified, the test will measure the maximum bandwidth for TCP and 10Mbps for UDP",
    )

    protocol: Optional[str] = Field(
        validation_alias="protocol",
        default=None,
        description="Transport protocol to use (tcp | udp)",
    )
