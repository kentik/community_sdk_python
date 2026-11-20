# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Snapshot import Snapshot


class GetDeviceConfigurationResponse(BaseModel):
    """
    GetDeviceConfigurationResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    config: Optional[Snapshot] = Field(validation_alias="config", default=None)
