# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .IdentityPredicate import IdentityPredicate
from .IpPredicate import IpPredicate
from .LabelPredicate import LabelPredicate
from .StringPredicate import StringPredicate


class SubjectPredicates(BaseModel):
    """
    Field predicates resolved relative to the parent ScopedClause.network_scope.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    deviceId: Optional[IdentityPredicate] = Field(
        validation_alias="deviceId", default=None
    )

    deviceName: Optional[StringPredicate] = Field(
        validation_alias="deviceName", default=None
    )

    deviceLabels: Optional[LabelPredicate] = Field(
        validation_alias="deviceLabels", default=None
    )

    siteId: Optional[IdentityPredicate] = Field(validation_alias="siteId", default=None)

    siteName: Optional[StringPredicate] = Field(
        validation_alias="siteName", default=None
    )

    interfaceId: Optional[IdentityPredicate] = Field(
        validation_alias="interfaceId", default=None
    )

    interfaceIndex: Optional[StringPredicate] = Field(
        validation_alias="interfaceIndex", default=None
    )

    interfaceName: Optional[StringPredicate] = Field(
        validation_alias="interfaceName", default=None
    )

    interfaceDescription: Optional[StringPredicate] = Field(
        validation_alias="interfaceDescription", default=None
    )

    ipAddress: Optional[IpPredicate] = Field(validation_alias="ipAddress", default=None)

    macAddress: Optional[StringPredicate] = Field(
        validation_alias="macAddress", default=None
    )
