# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GetPopulatorFieldResponse(BaseModel):
    """
    GetPopulatorFieldResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    totalCount: Optional[int] = Field(validation_alias="totalCount", default=None)

    offset: Optional[int] = Field(validation_alias="offset", default=None)

    limit: Optional[int] = Field(validation_alias="limit", default=None)

    extendedFields: Optional[Dict[str, Any]] = Field(
        validation_alias="extendedFields", default=None
    )
