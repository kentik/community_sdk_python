# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .BootstrapInfo import BootstrapInfo


class GenerateInstallCommandsResponse(BaseModel):
    """
    GenerateInstallCommandsResponse
    Response containing install commands ready to execute.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bootstrap: Optional[BootstrapInfo] = Field(
        validation_alias="bootstrap", default=None
    )
