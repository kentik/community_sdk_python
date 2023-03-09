"""
Examples of using the CloudExport API
"""

from examples.utils import client, pretty_print
from kentik_api.cloudexport.cloud_export import (
    AwsProperties,
    AzureProperties,
    CloudExport,
    CloudExportType,
    CloudProviderType,
    GceProperties,
)
from kentik_api.public.types import ID

PLAN_ID = ID("11467")


def cloud_exports_list() -> None:
    print("### CLOUD EXPORTS LIST")
    response = client().cloud_export.get_all()
    pretty_print(response)
    print()


def cloud_export_azure_crud() -> None:
    azure = AzureProperties(
        location="Singapore",
        resource_group="exampleresourcegroup",
        storage_account="examplestorageaccount",
        subscription_id=ID("bda574ce-5d2e-5d2c-83da-0f7b0762e10c"),
        security_principal_enabled=True,
    )
    export = CloudExport(
        name="community_sdk_python azure cloud export",
        type=CloudExportType.KENTIK_MANAGED,
        enabled=True,
        description="example azure cloud export",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.AZURE,
        azure=azure,
    )

    print("### AZURE CLOUD EXPORT CREATE")
    created_export = client().cloud_export.create(export)
    pretty_print(created_export)
    print()

    print("### AZURE CLOUD EXPORT GET")
    received_export = client().cloud_export.get(created_export.id)
    pretty_print(received_export)
    print()

    print("### AZURE CLOUD EXPORT PATCH")
    received_export.description = "PATCHED example azure cloud export"
    patched_export = client().cloud_export.patch(received_export, "export.description")
    pretty_print(patched_export)
    print()

    print("### AZURE CLOUD EXPORT UPDATE")
    received_export.name = "UPDATED community_sdk_python azure cloud export"
    updated_export = client().cloud_export.update(received_export)
    pretty_print(updated_export)
    print()

    print("### AZURE CLOUD EXPORT DELETE")
    client().cloud_export.delete(created_export.id)
    print("OK")
    print()


def cloud_export_aws_crud() -> None:
    aws = AwsProperties(
        bucket="cloudexport-src-s3-bucket",
        iam_role_arn="arn:aws:iam::177634097045:role/test-cloudexport-IngestRole",
        region="eu-central-1",
        delete_after_read=True,
        multiple_buckets=True,
    )
    export = CloudExport(
        name="community_sdk_python aws cloud export",
        type=CloudExportType.KENTIK_MANAGED,
        enabled=True,
        description="example aws cloud export",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.AWS,
        aws=aws,
    )

    print("### AWS CLOUD EXPORT CREATE")
    created_export = client().cloud_export.create(export)
    pretty_print(created_export)
    print()

    print("### AWS CLOUD EXPORT GET")
    received_export = client().cloud_export.get(created_export.id)
    pretty_print(received_export)
    print()

    print("### AWS CLOUD EXPORT PATCH")
    received_export.description = "PATCHED example aws cloud export"
    patched_export = client().cloud_export.patch(received_export, "export.description")
    pretty_print(patched_export)
    print()

    print("### AWS CLOUD EXPORT UPDATE")
    received_export.name = "UPDATED community_sdk_python aws cloud export"
    updated_export = client().cloud_export.update(received_export)
    pretty_print(updated_export)
    print()

    print("### AWS CLOUD EXPORT DELETE")
    client().cloud_export.delete(created_export.id)
    print("OK")
    print()


def cloud_export_gce_crud() -> None:
    gce = GceProperties(
        project="testproject",
        subscription="testsubscription",
    )
    export = CloudExport(
        name="community_sdk_python gce cloud export",
        type=CloudExportType.KENTIK_MANAGED,
        enabled=True,
        description="example gce cloud export",
        plan_id=PLAN_ID,
        cloud_provider=CloudProviderType.GCE,
        gce=gce,
    )

    print("### GCE CLOUD EXPORT CREATE")
    created_export = client().cloud_export.create(export)
    pretty_print(created_export)
    print()

    print("### GCE CLOUD EXPORT GET")
    received_export = client().cloud_export.get(created_export.id)
    pretty_print(received_export)
    print()

    print("### GCE CLOUD EXPORT PATCH")
    received_export.description = "PATCHED example gce cloud export"
    patched_export = client().cloud_export.patch(received_export, "export.description")
    pretty_print(patched_export)
    print()

    print("### GCE CLOUD EXPORT UPDATE")
    received_export.name = "UPDATED community_sdk_python gce cloud export"
    updated_export = client().cloud_export.update(received_export)
    pretty_print(updated_export)
    print()

    print("### GCE CLOUD EXPORT DELETE")
    client().cloud_export.delete(created_export.id)
    print("OK")
    print()


if __name__ == "__main__":
    cloud_exports_list()
    cloud_export_azure_crud()
    cloud_export_aws_crud()
    cloud_export_gce_crud()
