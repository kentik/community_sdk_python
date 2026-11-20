# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Interface import Interface


class ListInterfaceResponse(BaseModel):
    """
    ListInterfaceResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    interfaces: Optional[List[Optional[Interface]]] = Field(
        validation_alias="interfaces", default=None
    )

    totalCount: Optional[int] = Field(validation_alias="totalCount", default=None)

    invalidCount: Optional[int] = Field(validation_alias="invalidCount", default=None)
