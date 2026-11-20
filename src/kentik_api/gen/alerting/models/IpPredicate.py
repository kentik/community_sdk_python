# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .IpPredicateStringList import IpPredicateStringList


class IpPredicate(BaseModel):
    """
    Matches address.ip using canonical IP strings (IPv4 dotted decimal or IPv6 RFC 5952).
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not", serialization_alias="not", default=None
    )

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    in_: Optional[IpPredicateStringList] = Field(
        validation_alias="in", serialization_alias="in", default=None
    )

    within: Optional[str] = Field(
        validation_alias="within",
        default=None,
        description="True when the subject IP is contained within the given prefix (PostgreSQL: ip << cidr).",
    )

    withinAny: Optional[IpPredicateStringList] = Field(
        validation_alias="withinAny", default=None
    )
