# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Populator import Populator


class GetPopulatorResponse(BaseModel):
    """
    GetPopulatorResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    populator: Optional[Populator] = Field(validation_alias="populator", default=None)
