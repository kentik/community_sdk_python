# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class ChartResponse(BaseModel):
    """
    The result of a top-X chart query.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    dataUri: Optional[str] = Field(
        validation_alias="dataUri",
        default=None,
        description="The image as data:<mime>;base64,<data>.",
    )
