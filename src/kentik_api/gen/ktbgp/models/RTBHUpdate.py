# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .InetType import InetType
from .RTBHAction import RTBHAction
from .RTBHMatch import RTBHMatch


class RTBHUpdate(BaseModel):
    """
    RTBHUpdate model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    match: Optional[RTBHMatch] = Field(validation_alias="match", default=None)

    action: Optional[RTBHAction] = Field(validation_alias="action", default=None)

    creationTime: Optional[str] = Field(validation_alias="creationTime", default=None)

    inet: Optional[str] = Field(
        validation_alias="inet",
        default=None,
        description="deprecated: use inet_type instead",
    )

    inetType: Optional[InetType] = Field(validation_alias="inetType", default=None)

    key: Optional[str] = Field(
        validation_alias="key",
        default=None,
        description="mainly used for internal purposes",
    )
