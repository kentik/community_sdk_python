# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class CostProviderConcise(BaseModel):
    """
    CostProviderConcise
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="ID of the cost provider"
    )

    name: str = Field(validation_alias="name", description="Name of the cost provider")
