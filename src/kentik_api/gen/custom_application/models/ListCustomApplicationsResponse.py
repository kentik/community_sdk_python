# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CustomApplication import CustomApplication


class ListCustomApplicationsResponse(BaseModel):
    """
    ListCustomApplicationsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    applications: Optional[List[Optional[CustomApplication]]] = Field(
        validation_alias="applications", default=None
    )
