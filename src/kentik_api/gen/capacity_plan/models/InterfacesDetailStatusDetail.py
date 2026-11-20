# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class InterfacesDetailStatusDetail(BaseModel):
    """
    StatusDetail
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bps: Optional[str] = Field(
        validation_alias="bps", default=None, description="Bandwidth in bps"
    )

    count: Optional[int] = Field(
        validation_alias="count", default=None, description="Number of interfaces"
    )
