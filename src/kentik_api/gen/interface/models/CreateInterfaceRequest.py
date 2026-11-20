# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Interface import Interface


class CreateInterfaceRequest(BaseModel):
    """
    CreateInterfaceRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    interface: Optional[Interface] = Field(validation_alias="interface", default=None)
