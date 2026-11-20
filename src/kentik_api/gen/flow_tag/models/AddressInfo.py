# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class AddressInfo(BaseModel):
    """
    AddressInfo
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    addresses: Optional[List[str]] = Field(
        validation_alias="addresses",
        default=None,
        description="List of returning mac or ip address",
    )

    totalCount: Optional[int] = Field(
        validation_alias="totalCount",
        default=None,
        description="Total number of addresses available",
    )
