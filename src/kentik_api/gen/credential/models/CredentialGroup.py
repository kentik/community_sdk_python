# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Consumer import Consumer
from .CreatedBy import CreatedBy
from .Credential import Credential
from .CredentialType import CredentialType


class CredentialGroup(BaseModel):
    """
    CredentialGroup
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Pipe-delimited ids of the latest version of each credential in the group",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Credential group name"
    )

    version: Optional[int] = Field(
        validation_alias="version", default=None, description="Group version"
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Purpose of this credential group",
    )

    type: Optional[CredentialType] = Field(validation_alias="type", default=None)

    cdate: Optional[str] = Field(validation_alias="cdate", default=None)

    edate: Optional[str] = Field(validation_alias="edate", default=None)

    createdBy: Optional[CreatedBy] = Field(validation_alias="createdBy", default=None)

    labels: Optional[List[str]] = Field(
        validation_alias="labels", default=None, description="Label ids"
    )

    consumers: Optional[List[Optional[Consumer]]] = Field(
        validation_alias="consumers", default=None
    )

    credentials: Optional[List[Optional[Credential]]] = Field(
        validation_alias="credentials", default=None
    )
