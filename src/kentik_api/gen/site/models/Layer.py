# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class Layer(BaseModel):
    """
    Layer
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Name of the network layer"
    )

    deviceIds: Optional[List[str]] = Field(
        validation_alias="deviceIds",
        default=None,
        description="IDs of devices that are deemed to be part of the network layer",
    )
