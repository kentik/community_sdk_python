# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ASNDetails import ASNDetails


class GetASNDetailsResponse(BaseModel):
    """
    GetASNDetailsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asnDetails: Optional[ASNDetails] = Field(
        validation_alias="asnDetails", default=None
    )
