# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ConnectivityType import ConnectivityType
from .NetworkBoundary import NetworkBoundary


class ManualClassifyRequest(BaseModel):
    """
    Set connection type, network boundary, and provider of interface id(s) specified.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    interfaceIds: Optional[List[str]] = Field(
        validation_alias="interfaceIds",
        default=None,
        description="Interface ids to set the properties.",
    )

    connectivityType: Optional[ConnectivityType] = Field(
        validation_alias="connectivityType", default=None
    )

    networkBoundary: Optional[NetworkBoundary] = Field(
        validation_alias="networkBoundary", default=None
    )

    provider: Optional[str] = Field(
        validation_alias="provider", default=None, description="Network provider."
    )
