# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .CommandAcl import CommandAcl


class GetCommandAclsResponse(BaseModel):
    """
    GetCommandAclsResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    acls: Optional[List[Optional[CommandAcl]]] = Field(
        validation_alias="acls", default=None
    )
