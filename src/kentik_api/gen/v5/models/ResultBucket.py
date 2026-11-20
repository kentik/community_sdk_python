# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ResultBucket(BaseModel):
    """
    The rows of one bucket.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    bucket: Optional[str] = Field(
        validation_alias="bucket",
        default=None,
        description="The bucket name from the request.",
    )

    data: Optional[List[Dict[str, Any]]] = Field(
        validation_alias="data",
        default=None,
        description="One row per result. The keys depend on the query: the dimension columns, key, the aggregate columns, and timeSeries for the top-X rows.",
    )
