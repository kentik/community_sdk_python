# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class CustomApplication(BaseModel):
    """
    CustomApplication model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the custom application.",
    )

    name: str = Field(
        validation_alias="name", description="A unique name for the custom application."
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="An optional description for the custom application.",
    )

    ipRange: Optional[List[str]] = Field(
        validation_alias="ipRange",
        default=None,
        description="List of IP addresses in IP/CIDR format.",
    )

    protocol: Optional[List[int]] = Field(
        validation_alias="protocol",
        default=None,
        description="List of Protocol numbers.",
    )

    port: Optional[List[int]] = Field(
        validation_alias="port", default=None, description="List of Port numbers."
    )

    asn: Optional[List[int]] = Field(
        validation_alias="asn", default=None, description="List of ASNs."
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Date-time of custom application creation, in UTC.",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Date-time of most-recent custom application edit, in UTC.",
    )

    userId: Optional[str] = Field(
        validation_alias="userId",
        default=None,
        description="User ID associated with this custom application.",
    )
