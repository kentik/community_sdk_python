# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Test import Test


class ListTestsResponse(BaseModel):
    """
    ListTestsResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tests: Optional[List[Optional[Test]]] = Field(
        validation_alias="tests",
        default=None,
        description="List of configured active or paused tests",
    )

    invalidCount: Optional[int] = Field(
        validation_alias="invalidCount",
        default=None,
        description="Number of invalid entries encountered while collecting data",
    )
