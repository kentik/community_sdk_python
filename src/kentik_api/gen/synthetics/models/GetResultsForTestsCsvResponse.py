# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class GetResultsForTestsCsvResponse(BaseModel):
    """
    GetResultsForTestsCsvResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    contentType: Optional[str] = Field(
        validation_alias="contentType",
        default=None,
        description="Content type of the response hardcoded to 'text/csv'",
    )

    data: Optional[str] = Field(
        validation_alias="data", default=None, description="CSV data as byte array"
    )
