# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class HTTPResponseData(BaseModel):
    """
    HTTPResponseData
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    status: Optional[int] = Field(
        validation_alias="status", default=None, description="HTTP status in response"
    )

    size: Optional[int] = Field(
        validation_alias="size",
        default=None,
        description="Total size of  received response body",
    )

    data: Optional[str] = Field(
        validation_alias="data",
        default=None,
        description="Detailed information about transaction timing, connection characteristics and response",
    )
