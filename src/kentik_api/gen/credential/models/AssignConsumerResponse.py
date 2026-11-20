# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .Credential import Credential


class AssignConsumerResponse(BaseModel):
    """
    AssignConsumerResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    credential: Optional[Credential] = Field(
        validation_alias="credential", default=None
    )
