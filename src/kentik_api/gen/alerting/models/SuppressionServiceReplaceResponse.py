# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Suppression import Suppression


class SuppressionServiceReplaceResponse(BaseModel):
    """
    SuppressionServiceReplaceResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    suppression: Optional[Suppression] = Field(
        validation_alias="suppression", default=None
    )
