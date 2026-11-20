# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .ChannelType import ChannelType


class SearchNotificationChannelsRequest(BaseModel):
    """
    SearchNotificationChannelsRequest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    namePattern: Optional[str] = Field(
        validation_alias="namePattern",
        default=None,
        description="Regular expression pattern for matching the name attribute of channels. Empty string matches any name, otherwise the regular expression must consume all characters in the channel name.",
    )

    types: Optional[List[Optional[ChannelType]]] = Field(
        validation_alias="types",
        default=None,
        description="List of ChannelType enum values to match. Empty list matches any channel type.",
    )

    includeDisabled: Optional[bool] = Field(
        validation_alias="includeDisabled",
        default=None,
        description="Include disabled channels in results.",
    )
