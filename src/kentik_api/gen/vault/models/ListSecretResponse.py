# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Secret import Secret


class ListSecretResponse(BaseModel):
    """
    ListSecretResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    secrets: List[Secret] = Field(
        validation_alias="secrets", description="List of secrets"
    )

    invalidCredentialCount: Optional[int] = Field(
        validation_alias="invalidCredentialCount",
        default=None,
        description="Number of objects with invalid data (which are not returned in the response).",
    )
