# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List

from pydantic import BaseModel, Field

from .QueryItem import QueryItem


class QueryRequest(BaseModel):
    """
    The body of a top-X data or URL query.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    queries: List[QueryItem] = Field(
        validation_alias="queries", description="One item for each series. Usually one."
    )
