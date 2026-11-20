# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CredentialOverview import CredentialOverview


class ListCredentialOverviewsResponse(BaseModel):
    """
    ListCredentialOverviewsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    overviews: Optional[List[Optional[CredentialOverview]]] = Field(
        validation_alias="overviews", default=None
    )
