# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .Alert import Alert
from .Asset import Asset
from .TenantLink import TenantLink


class Package(BaseModel):
    """
    Package
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="Unique system assigned identifier of the package",
    )

    companyId: Optional[str] = Field(
        validation_alias="companyId",
        default=None,
        description="Company id of the associated package",
    )

    name: Optional[str] = Field(
        validation_alias="name", default=None, description="Name of package template"
    )

    description: Optional[str] = Field(
        validation_alias="description",
        default=None,
        description="Description of package template",
    )

    icon: Optional[str] = Field(
        validation_alias="icon", default=None, description="Icon to display"
    )

    color: Optional[str] = Field(
        validation_alias="color", default=None, description="Color of Icon"
    )

    alerts: Optional[List[Optional[Alert]]] = Field(
        validation_alias="alerts",
        default=None,
        description="Alert thresholds and policies",
    )

    assets: Optional[Asset] = Field(validation_alias="assets", default=None)

    isDefault: Optional[bool] = Field(
        validation_alias="isDefault", default=None, description="Is default template"
    )

    tenants: Optional[List[Optional[TenantLink]]] = Field(
        validation_alias="tenants", default=None, description="Tenant link information"
    )
