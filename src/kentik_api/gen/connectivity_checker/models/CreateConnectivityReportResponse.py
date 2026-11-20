# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class CreateConnectivityReportResponse(BaseModel):
    """
    CreateConnectivityReportResponse
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    reachable: Optional[bool] = Field(
        validation_alias="reachable",
        default=None,
        description="Attribute controlling whether the instance is active",
    )

    returnReachable: Optional[bool] = Field(
        validation_alias="returnReachable",
        default=None,
        description="Attribute controlling whether the instance is active",
    )

    queryStatus: Optional[str] = Field(
        validation_alias="queryStatus", default=None, description="Status of the query."
    )

    reportUrl: Optional[str] = Field(
        validation_alias="reportUrl",
        default=None,
        description="URL to view the connectivity checker report in the Kentik platform.",
    )

    paths: Optional[List[str]] = Field(
        validation_alias="paths",
        default=None,
        description="The connection paths in your network.",
    )

    returnPaths: Optional[List[str]] = Field(
        validation_alias="returnPaths",
        default=None,
        description="The return connection paths in your network.",
    )

    lastMetadataFetch: Optional[str] = Field(
        validation_alias="lastMetadataFetch",
        default=None,
        description="The timestamp indicating when the metadata used to build the connectivity checker report was last fetched.",
    )
