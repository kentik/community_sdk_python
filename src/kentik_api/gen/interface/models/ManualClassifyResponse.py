# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class ManualClassifyResponse(BaseModel):
    """
    ManualClassifyResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceIds: Optional[List[str]] = Field(validation_alias="deviceIds", default=None)
