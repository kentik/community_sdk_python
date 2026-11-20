# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from pydantic import BaseModel, Field

from .Suppression import Suppression


class SuppressionServiceCreateRequest(BaseModel):
    """
    SuppressionServiceCreateRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    suppression: Suppression = Field(validation_alias="suppression")
