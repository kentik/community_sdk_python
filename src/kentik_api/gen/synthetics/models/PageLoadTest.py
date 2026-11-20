# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PageLoadTest(BaseModel):
    """
    PageLoadTest
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    target: Optional[str] = Field(
        validation_alias="target",
        default=None,
        description="HTTP or HTTPS URL to request",
    )

    timeout: Optional[int] = Field(
        validation_alias="timeout",
        default=None,
        description="HTTP transaction timeout (in milliseconds)",
    )

    headers: Optional[Dict[str, Any]] = Field(
        validation_alias="headers",
        default=None,
        description="Map of HTTP header values keyed by header names",
    )

    ignoreTlsErrors: Optional[bool] = Field(
        validation_alias="ignoreTlsErrors",
        default=None,
        description="Boolean indicating whether to ignore TLS certificate verification errors",
    )

    cssSelectors: Optional[Dict[str, Any]] = Field(
        validation_alias="cssSelectors",
        default=None,
        description="Map of CSS selector values keyed by selector name",
    )
