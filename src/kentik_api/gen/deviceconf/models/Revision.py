# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field


class Revision(BaseModel):
    """
    TODO: I somewhat regret embedding "Revision" inside "Snapshot".
    Being embedded means that any time we add something to Revision, it affects
    Snapshot as well. For example, when we added device_id to Revision, it
    meant that now Snapshot has device_id in two places (top-level and inside
    Revision). At some point we should probably flatten these fields into the
    top-level Snapshot message and deprecate the embedded Revision message. (Or
    break the coupling between Snapshot and List Revisions some other way.)
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: Optional[str] = Field(
        validation_alias="id",
        default=None,
        description="incremented for each different configuration fetched from the device",
    )

    lastFetched: Optional[str] = Field(validation_alias="lastFetched", default=None)

    firstFetched: Optional[str] = Field(validation_alias="firstFetched", default=None)

    deviceId: Optional[str] = Field(validation_alias="deviceId", default=None)
