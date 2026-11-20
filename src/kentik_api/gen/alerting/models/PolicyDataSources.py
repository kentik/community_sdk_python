# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field

from .PolicyDataSourcesDeviceTag import PolicyDataSourcesDeviceTag


class PolicyDataSources(BaseModel):
    """
    PolicyDataSources model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    allDevices: Optional[bool] = Field(
        validation_alias="allDevices",
        default=None,
        description="If true, all devices traffic will be included in the policy and the other fields will be ignored.",
    )

    deviceIds: Optional[List[str]] = Field(
        validation_alias="deviceIds",
        default=None,
        description="The IDs of the devices to include in the policy.",
    )

    labelIds: Optional[List[str]] = Field(
        validation_alias="labelIds",
        default=None,
        description="The IDs of the labels to include in the policy.",
    )

    siteIds: Optional[List[str]] = Field(
        validation_alias="siteIds",
        default=None,
        description="The IDs of the sites to include in the policy.",
    )

    types: Optional[List[str]] = Field(
        validation_alias="types",
        default=None,
        description="The types of devices to include in the policy.",
    )

    deviceTags: Optional[List[Optional[PolicyDataSourcesDeviceTag]]] = Field(
        validation_alias="deviceTags",
        default=None,
        description="[Not implemented] The device tags to include in the policy. If multiple tags are specified, the policy will include devices that match at least one of the tags.",
    )
