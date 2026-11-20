# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .CommitDetails import CommitDetails
from .ConfigEncoding import ConfigEncoding
from .DevicePlatform import DevicePlatform
from .Revision import Revision


class Snapshot(BaseModel):
    """
    Snapshot model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    agentId: Optional[str] = Field(
        validation_alias="agentId",
        default=None,
        description="Agent that fetched the configuration",
    )

    deviceId: Optional[str] = Field(validation_alias="deviceId", default=None)

    revision: Optional[Revision] = Field(validation_alias="revision", default=None)

    fetchError: Optional[bool] = Field(
        validation_alias="fetchError",
        default=None,
        description="error message is in config_data if true",
    )

    encoding: Optional[ConfigEncoding] = Field(
        validation_alias="encoding", default=None
    )

    configData: Optional[str] = Field(validation_alias="configData", default=None)

    digest: Optional[str] = Field(
        validation_alias="digest",
        default=None,
        description="SHA256 digest of config_data",
    )

    diffData: Optional[str] = Field(validation_alias="diffData", default=None)

    diffRevision: Optional[Revision] = Field(
        validation_alias="diffRevision", default=None
    )

    firstFetched: Optional[str] = Field(
        validation_alias="firstFetched",
        default=None,
        description="Deprecated: use revision.first_fetched instead",
    )

    commitDetails: Optional[CommitDetails] = Field(
        validation_alias="commitDetails", default=None
    )

    platform: Optional[DevicePlatform] = Field(
        validation_alias="platform", default=None
    )
