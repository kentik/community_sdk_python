# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .LandingType import LandingType
from .PermissionEntry import PermissionEntry
from .Role import Role


class User(BaseModel):
    """
    User
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="System generated unique identifier",
    )

    userEmail: str = Field(
        validation_alias="userEmail",
        description="User e-mail address (serves also as username)",
    )

    userFullName: str = Field(validation_alias="userFullName", description="Full name")

    role: Role = Field(validation_alias="role")

    permissions: Optional[List[Optional[PermissionEntry]]] = Field(
        validation_alias="permissions",
        default=None,
        description="Legacy permissions granted to the user (deprecated, use rbac roles and role-sets)",
    )

    filter: Optional[str] = Field(
        validation_alias="filter",
        default=None,
        description="Optional JSON string defining filter for objects visible to the user",
    )

    lastLogin: Optional[str] = Field(
        validation_alias="lastLogin",
        default=None,
        description="UTC Timestamp of user's last login session",
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    defaultLandingPageType: Optional[LandingType] = Field(
        validation_alias="defaultLandingPageType", default=None
    )

    defaultLandingPageValue: Optional[str] = Field(
        validation_alias="defaultLandingPageValue",
        default=None,
        description="Identifier of the specific landing page. Applies to Dashboard, Quick View, Saved View, and Observation Deck landing page types.",
    )

    roles: Optional[List[str]] = Field(
        validation_alias="roles", default=None, description="List of RBAC roles."
    )

    roleSets: Optional[List[str]] = Field(
        validation_alias="roleSets", default=None, description="List of RBAC role sets."
    )
