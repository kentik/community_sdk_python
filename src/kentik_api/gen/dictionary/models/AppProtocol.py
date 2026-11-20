# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AppProtocolMetadata import AppProtocolMetadata


class AppProtocol(BaseModel):
    """
    AppProtocol model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique identifier for the app protocol",
    )

    displayName: Optional[str] = Field(
        validation_alias="displayName",
        default=None,
        description="Human-readable display name",
    )

    addToStandardFields: Optional[bool] = Field(
        validation_alias="addToStandardFields",
        default=None,
        description="When true, this AppProtocol is able to use shared fields",
    )

    status: Optional[str] = Field(
        validation_alias="status",
        default=None,
        description="Will always be 'A' for Active",
    )

    metadata: Optional[AppProtocolMetadata] = Field(
        validation_alias="metadata", default=None
    )
