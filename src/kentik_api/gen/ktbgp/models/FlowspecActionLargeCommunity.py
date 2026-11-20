# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class FlowspecActionLargeCommunity(BaseModel):
    """
    FlowspecActionLargeCommunity
    BGP Large Communities attribute encoded as an unordered set of one or more
    twelve-octet values, each consisting of a four-octet Global
    Administrator field and two four-octet operator-defined fields, each
    of which can be used to denote properties or actions significant to
    the operator of the AS assigning the values.
    https://datatracker.ietf.org/doc/html/rfc8092
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn: Optional[int] = Field(validation_alias="asn", default=None)

    data1: Optional[int] = Field(validation_alias="data1", default=None)

    data2: Optional[int] = Field(validation_alias="data2", default=None)
