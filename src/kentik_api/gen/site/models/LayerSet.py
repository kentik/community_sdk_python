# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Layer import Layer


class LayerSet(BaseModel):
    """
    LayerSet
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    layers: Optional[List[Optional[Layer]]] = Field(
        validation_alias="layers",
        default=None,
        description="List of parallel network layers",
    )
