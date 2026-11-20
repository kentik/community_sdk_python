# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Plan import Plan


class ListPlansResponse(BaseModel):
    """
    ListPlansResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    plans: Optional[List[Optional[Plan]]] = Field(
        validation_alias="plans", default=None
    )
