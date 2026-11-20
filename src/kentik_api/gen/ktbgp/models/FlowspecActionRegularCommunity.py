# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionRegularCommunity(BaseModel):
    """
    FlowspecActionRegularCommunity
    Extenstion of the two-octed AS numbers as four-octed entinties.
    https://datatracker.ietf.org/doc/html/rfc6793
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn1: Optional[int] = Field(validation_alias="asn1", default=None)

    asn2: Optional[int] = Field(validation_alias="asn2", default=None)
