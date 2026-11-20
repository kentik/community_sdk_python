# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .ResultFormat import ResultFormat
from .ResultType import ResultType


class GetJourneysNlqResponse(BaseModel):
    """
    GetJourneysNlqResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    result: Optional[str] = Field(validation_alias="result", default=None)

    resultType: Optional[ResultType] = Field(
        validation_alias="resultType", default=None
    )

    resultFormat: Optional[ResultFormat] = Field(
        validation_alias="resultFormat", default=None
    )
