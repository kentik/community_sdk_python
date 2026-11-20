# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Optional

from pydantic import BaseModel, Field

from .AttributeFilterStringArray import AttributeFilterStringArray


class AttributeFilter(BaseModel):
    """
    AttributeFilter model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    not_: Optional[bool] = Field(
        validation_alias="not",
        serialization_alias="not",
        default=None,
        description="Please note attribute filter operates on strings or stringified values",
    )

    empty: Optional[bool] = Field(
        validation_alias="empty",
        default=None,
        description='Indicates that we want to check for an empty value.  To use empty this value MUST be set to\ntrue.  Setting not to true enables us to look for "not-empty".',
    )

    equals: Optional[str] = Field(validation_alias="equals", default=None)

    startsWith: Optional[str] = Field(validation_alias="startsWith", default=None)

    endsWith: Optional[str] = Field(validation_alias="endsWith", default=None)

    contains: Optional[str] = Field(validation_alias="contains", default=None)

    in_: Optional[AttributeFilterStringArray] = Field(
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
        description='The equivalent of: value="*.  To use any this value MUST be set to true. Setting not to true\nenables us to look for "not-anything", but that predicate does not make much sense.',
    )
