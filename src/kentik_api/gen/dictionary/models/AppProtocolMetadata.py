# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class AppProtocolMetadata(BaseModel):
    """
    AppProtocolMetadata model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    fullDataOnly: Optional[bool] = Field(
        validation_alias="fullDataOnly",
        default=None,
        description="If true, this AppProtocol can only be used with Full Data, not Fast Data",
    )
