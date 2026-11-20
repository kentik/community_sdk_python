# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class IpTest(BaseModel):
    """
    IpTest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    targets: Optional[List[str]] = Field(
        validation_alias="targets",
        default=None,
        description="List of IP addresses of targets",
    )

    useLocalIp: Optional[bool] = Field(
        validation_alias="useLocalIp",
        default=None,
        description="Boolean value indicating whether to use local (private) IP address of the target agents",
    )
