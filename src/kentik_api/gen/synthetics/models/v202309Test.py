# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .UserInfo import UserInfo
from .v202309TestSettings import v202309TestSettings
from .v202309TestStatus import v202309TestStatus


class v202309Test(BaseModel):
    """
    Test
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id", default=None, description="Unique ID of the test"
    )

    name: Optional[str] = Field(
        validation_alias="name",
        default=None,
        description="User selected name of the test",
    )

    type: Optional[str] = Field(
        validation_alias="type", default=None, description="Type of the test"
    )

    status: Optional[v202309TestStatus] = Field(validation_alias="status", default=None)

    settings: Optional[v202309TestSettings] = Field(
        validation_alias="settings", default=None
    )

    cdate: Optional[str] = Field(
        validation_alias="cdate", default=None, description="Creation timestamp (UTC)"
    )

    edate: Optional[str] = Field(
        validation_alias="edate",
        default=None,
        description="Last modification timestamp (UTC)",
    )

    createdBy: Optional[UserInfo] = Field(validation_alias="createdBy", default=None)

    lastUpdatedBy: Optional[UserInfo] = Field(
        validation_alias="lastUpdatedBy", default=None
    )

    labels: Optional[List[str]] = Field(
        validation_alias="labels",
        default=None,
        description="Set of labels associated with the test",
    )
