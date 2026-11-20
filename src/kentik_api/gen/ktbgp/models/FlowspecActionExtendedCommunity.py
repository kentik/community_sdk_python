# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ExtendedCommunityRouteType import ExtendedCommunityRouteType


class FlowspecActionExtendedCommunity(BaseModel):
    """
    FlowspecActionExtendedCommunity
    The attribute consists of a set of "extended communities".
    All routes with the Extended Communities attribute belong to
    the communities listed in the attribute.
    https://datatracker.ietf.org/doc/html/rfc4360
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    routeType: Optional[ExtendedCommunityRouteType] = Field(
        validation_alias="routeType", default=None
    )

    asn1: Optional[int] = Field(validation_alias="asn1", default=None)

    asn2: Optional[int] = Field(validation_alias="asn2", default=None)
