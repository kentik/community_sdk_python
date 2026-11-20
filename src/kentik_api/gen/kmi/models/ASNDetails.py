# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CustomerProvider import CustomerProvider
from .Peer import Peer


class ASNDetails(BaseModel):
    """
    ASNDetails
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

    countryName: Optional[str] = Field(
        validation_alias="countryName",
        default=None,
        description="Country Name of the Autonomous System",
    )

    customers: Optional[List[Optional[CustomerProvider]]] = Field(
        validation_alias="customers", default=None, description="List of Customers"
    )

    providers: Optional[List[Optional[CustomerProvider]]] = Field(
        validation_alias="providers", default=None, description="List of Providers"
    )

    peers: Optional[List[Optional[Peer]]] = Field(
        validation_alias="peers", default=None, description="List of Peers"
    )
