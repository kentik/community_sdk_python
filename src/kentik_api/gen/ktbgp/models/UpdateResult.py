# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AdvertStatus import AdvertStatus


class UpdateResult(BaseModel):
    """
    UpdateResult model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceId: Optional[str] = Field(validation_alias="deviceId", default=None)

    status: Optional[AdvertStatus] = Field(validation_alias="status", default=None)

    message: Optional[str] = Field(validation_alias="message", default=None)
