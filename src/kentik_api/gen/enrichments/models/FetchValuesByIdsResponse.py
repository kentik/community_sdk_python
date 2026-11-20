# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FetchValuesByIdsResponse(BaseModel):
    """
    FetchValuesByIdsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    values: Optional[Dict[str, Any]] = Field(
        validation_alias="values",
        default=None,
        description="Mapping from lookup ID (decimal string) to the corresponding string value. IDs that did not resolve for the caller's company are absent from the map; callers must handle missing keys.",
    )
