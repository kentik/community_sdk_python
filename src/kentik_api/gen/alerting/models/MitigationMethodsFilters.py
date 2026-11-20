# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .MitigationPlatformType import MitigationPlatformType
from .TimeRange import TimeRange


class MitigationMethodsFilters(BaseModel):
    """
    MitigationMethodsFilters model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    methodIds: Optional[List[str]] = Field(
        validation_alias="methodIds",
        default=None,
        description="The IDs of the mitigation methods to list.",
    )

    platformTypes: Optional[List[Optional[MitigationPlatformType]]] = Field(
        validation_alias="platformTypes",
        default=None,
        description="The platform types the mitigation methods are associated with.",
    )

    createdAt: Optional[TimeRange] = Field(validation_alias="createdAt", default=None)

    modifiedAt: Optional[TimeRange] = Field(validation_alias="modifiedAt", default=None)
