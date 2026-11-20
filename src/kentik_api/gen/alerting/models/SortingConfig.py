# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .SortingConfigField import SortingConfigField


class SortingConfig(BaseModel):
    """
    SortingConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    fields: Optional[List[Optional[SortingConfigField]]] = Field(
        validation_alias="fields", default=None
    )
