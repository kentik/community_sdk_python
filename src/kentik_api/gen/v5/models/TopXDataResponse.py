# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ResultBucket import ResultBucket


class TopXDataResponse(BaseModel):
    """
    The result of a top-X data query.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    results: Optional[List[Optional[ResultBucket]]] = Field(
        validation_alias="results", default=None
    )
