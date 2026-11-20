# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Alert import Alert
from .Asset import Asset
from .CustomDimension import CustomDimension
from .Devices import Devices
from .Filter import Filter
from .Package import Package
from .User import User


class Tenant(BaseModel):
    """
    Tenant
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique system assigned identifier of the tenant",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId",
        default=None,
        description="Company id of the associated package",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Name of tenant"
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Description of tenant",
    )

    type: Optional[str] = Field(
        validation_alias="type", default=None, description="Subtenant"
    )

    enabled: Optional[bool] = Field(
        validation_alias="enabled",
        default=None,
        description="Is tenant actively enable",
    )

    alerts: Optional[List[Optional[Alert]]] = Field(
        validation_alias="alerts",
        default=None,
        description="config object\n\nAlert thresholds and policies",
    )

    assets: Optional[Asset] = Field(validation_alias="assets", default=None)

    asn: Optional[str] = Field(
        validation_alias="asn", default=None, description="ASN data source."
    )

    cidr: Optional[str] = Field(
        validation_alias="cidr", default=None, description="CIDR data source."
    )

    customDimensions: Optional[List[Optional[CustomDimension]]] = Field(
        validation_alias="customDimensions",
        default=None,
        description="Custom dimension data source",
    )

    devices: Optional[Devices] = Field(validation_alias="devices", default=None)

    filters: Optional[Filter] = Field(validation_alias="filters", default=None)

    interfaceName: Optional[str] = Field(
        validation_alias="interfaceName",
        default=None,
        description="Interface data source.",
    )

    snmpAlias: Optional[str] = Field(
        validation_alias="snmpAlias", default=None, description="SNMP data source."
    )

    packages: Optional[List[Optional[Package]]] = Field(
        validation_alias="packages",
        default=None,
        description="Packages associated with the tenant.",
    )

    users: Optional[List[Optional[User]]] = Field(
        validation_alias="users",
        default=None,
        description="Users associated with the tenant (deprecated; use ListTenantUser).",
    )

    templateId: Optional[str] = Field(
        validation_alias="templateId",
        default=None,
        description="Package template ID to assign with tenant.",
    )
