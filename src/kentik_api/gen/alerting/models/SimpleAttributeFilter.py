# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .SimpleAttributeFilterStringArray import SimpleAttributeFilterStringArray


class SimpleAttributeFilter(BaseModel):
    """
    SimpleAttributeFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    startsWith: Optional[str] = Field(validation_alias="startsWith", default=None)

    endsWith: Optional[str] = Field(validation_alias="endsWith", default=None)

    contains: Optional[str] = Field(validation_alias="contains", default=None)

    in_: Optional[SimpleAttributeFilterStringArray] = Field(
        validation_alias="in", serialization_alias="in", default=None
    )

    matchesRegex: Optional[str] = Field(
        validation_alias="matchesRegex",
        default=None,
        description="Unanchored: the pattern may match anywhere in the value (`foo` matches\n`xfooy`). Use `^` / `$` to require the start or end of the string.\nCommon dialect for all use cases.\nSupported regex features: literals, `.`, `|`, `()` / `(?:)`, `*+?{n,m}`,\n`^$`, POSIX classes, `\\d \\D \\s \\S \\w \\W`.\nUnsupported regex features: `\\b \\B \\A \\z \\Q \\E \\p \\P`, and `(?` other than `(?:)`.",
    )

    any: Optional[bool] = Field(
        validation_alias="any",
        default=None,
        description='The equivalent of: value="*.  To use any this value MUST be set to true.',
    )
