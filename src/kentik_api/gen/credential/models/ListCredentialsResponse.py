# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Credential import Credential


class ListCredentialsResponse(BaseModel):
    """
    ListCredentialsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    credentials: Optional[List[Optional[Credential]]] = Field(
        validation_alias="credentials", default=None
    )
