# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Insight(BaseModel):
    """
    Insight
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    asn: Optional[int] = Field(
        validation_alias="asn",
        default=None,
        description="Autonomous System Number (ASN)",
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="Name of the Autonomous System",
    )

    type: Optional[int] = Field(
        validation_alias="type", default=None, description="Type of insight"
    )

    message: Optional[str] = Field(
        validation_alias="message", default=None, description="Insight message text"
    )

    createdAt: Optional[str] = Field(
        validation_alias="createdAt",
        default=None,
        description="Timestamp when insight was created",
    )
