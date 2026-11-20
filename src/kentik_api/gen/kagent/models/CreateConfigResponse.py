# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Config import Config


class CreateConfigResponse(BaseModel):
    """
    CreateConfigResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    config: Optional[Config] = Field(validation_alias="config", default=None)
