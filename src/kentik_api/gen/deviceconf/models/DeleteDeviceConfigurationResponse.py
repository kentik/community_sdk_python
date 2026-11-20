# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Revision import Revision


class DeleteDeviceConfigurationResponse(BaseModel):
    """
    DeleteDeviceConfigurationResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    orphanedRevision: Optional[Revision] = Field(
        validation_alias="orphanedRevision", default=None
    )
