# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class NmsContextDatasetInfo(BaseModel):
    """
    NmsContextDatasetInfo model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    customType: Optional[bool] = Field(validation_alias="customType", default=None)

    dimensions: Optional[List[str]] = Field(validation_alias="dimensions", default=None)

    entityType: Optional[str] = Field(validation_alias="entityType", default=None)

    measurements: Optional[List[str]] = Field(
        validation_alias="measurements", default=None
    )
