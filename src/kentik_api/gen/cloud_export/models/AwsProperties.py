# AUTO-GENERATED: openapi-python-generator, model generation
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from typing import List, Optional

from pydantic import BaseModel, Field


class AwsProperties(BaseModel):
    """
    AwsProperties
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    iamRoleArn: str = Field(
        validation_alias="iamRoleArn",
        description="ARN of the IAM role granted access to the S3 bucket and describe API end-points.",
    )

    region: str = Field(
        validation_alias="region",
        description="Name of AWS region from which to export flow logs.",
    )

    metadataOnly: Optional[bool] = Field(
        validation_alias="metadataOnly",
        default=None,
        description="Import only metadata without any flows (default false).",
    )

    collectFlowLogs: Optional[bool] = Field(
        validation_alias="collectFlowLogs",
        default=None,
        description="Import metadata and collect flow logs (default true).",
    )

    collectFirewallLogs: Optional[bool] = Field(
        validation_alias="collectFirewallLogs",
        default=None,
        description="Import metadata and collect firewall logs in addition to flow logs (default false). Note that in order to collect firewall logs without collection of flow logs, collect_flow_logs must be set to false.",
    )

    collectMetrics: Optional[bool] = Field(
        validation_alias="collectMetrics",
        default=None,
        description="Import metadata and collect metrics data.  Note that flow logs will still be collected unless metadata_only is also set to true. (default false).",
    )

    bucket: Optional[str] = Field(
        validation_alias="bucket",
        default=None,
        description="Name of S3 bucket from which flow and/or firewall logs are to be exported.",
    )

    bucketPrefix: Optional[str] = Field(
        validation_alias="bucketPrefix",
        default=None,
        description="Prefix of S3 bucket from which flow and/or firewall logs are to be exported.",
    )

    deleteAfterRead: Optional[bool] = Field(
        validation_alias="deleteAfterRead",
        default=None,
        description="Delete from logs from the S3 bucket after export (default false).",
    )

    awsIamRoleArnIsOrg: Optional[bool] = Field(
        validation_alias="awsIamRoleArnIsOrg",
        default=None,
        description="Iam role is organization role (default false).",
    )

    secondaryAwsAccounts: Optional[List[str]] = Field(
        validation_alias="secondaryAwsAccounts",
        default=None,
        description="Accounts ids granted access to the describe API end-points.",
    )

    secondaryAwsBlockedAccounts: Optional[List[str]] = Field(
        validation_alias="secondaryAwsBlockedAccounts",
        default=None,
        description="Accounts ids that should be filtered from organization when running describe API end-points.",
    )

    secondaryAwsRegions: Optional[List[str]] = Field(
        validation_alias="secondaryAwsRegions",
        default=None,
        description="Regions of secondary accounts from which to collect metadata.",
    )

    secondaryAwsSuffix: Optional[str] = Field(
        validation_alias="secondaryAwsSuffix",
        default=None,
        description="Used to generate secondary account ARN based on template arn:aws:iam::<<aws_account_id>>:role/<<role_suffix>>",
    )
