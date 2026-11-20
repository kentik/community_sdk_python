# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Nlri import Nlri


class GetRoutesForTargetRequest(BaseModel):
    """
    GetRoutesForTargetRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    time: str = Field(
        validation_alias="time",
        description="Reference UTC time for the route information snapshot",
    )

    target: Nlri = Field(validation_alias="target")

    includeCovered: Optional[bool] = Field(
        validation_alias="includeCovered",
        default=None,
        description="Return routes for subnets (sub-prefixes) of the target prefix (default: false)",
    )

    checkRpki: Optional[bool] = Field(
        validation_alias="checkRpki",
        default=None,
        description="Return information about validity of prefix advertisements with respect to RPKI (default: false)",
    )
