# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AclAction import AclAction
from .AclMode import AclMode


class CommandAcl(BaseModel):
    """
    CommandAcl model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    action: Optional[AclAction] = Field(validation_alias="action", default=None)

    mode: Optional[AclMode] = Field(validation_alias="mode", default=None)

    filter: Optional[str] = Field(validation_alias="filter", default=None)
