# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .AutonomousSystem import AutonomousSystem


class ASGroupDetailed(BaseModel):
    """
    ASGroupDetailed
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="System generated unique identifier",
    )

    name: str = Field(validation_alias="name", description="User selected unique name")

    asn: Optional[List[Optional[AutonomousSystem]]] = Field(
        validation_alias="asn", default=None, description="List of ASNs"
    )

    createdDate: Optional[str] = Field(
        validation_alias="createdDate",
        default=None,
        description="Creation timestamp (UTC)",
    )

    updatedDate: Optional[str] = Field(
        validation_alias="updatedDate",
        default=None,
        description="Last modification timestamp (UTC)",
    )
