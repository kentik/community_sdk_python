# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Scope import Scope


class ListScopesResponse(BaseModel):
    """
    ListScopesResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    scopes: Optional[List[Optional[Scope]]] = Field(
        validation_alias="scopes",
        default=None,
        description="The company's Focus Scopes.",
    )
