# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .TestSettings import TestSettings
from .TestStatus import TestStatus
from .UserInfo import UserInfo


class Test(BaseModel):
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

    status: Optional[TestStatus] = Field(validation_alias="status", default=None)

    settings: Optional[TestSettings] = Field(validation_alias="settings", default=None)

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
