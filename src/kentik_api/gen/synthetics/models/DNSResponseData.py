# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class DNSResponseData(BaseModel):
    """
    DNSResponseData
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: Optional[int] = Field(
        validation_alias="status", default=None, description="Received DNS status"
    )

    data: Optional[str] = Field(
        validation_alias="data",
        default=None,
        description="Text rendering of received DNS resolution",
    )
