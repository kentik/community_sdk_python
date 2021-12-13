"""
Examples of using the CloudExport API
"""

from examples.utils import client, pretty_print
from kentik_api.cloudexport.cloud_export import AzureProperties, CloudExport, CloudExportType
from kentik_api.public.types import ID


def cloud_exports_list() -> None:
    print("### CLOUD EXPORTS LIST")
    response = client().cloud_export.get_all()
    pretty_print(response)
    print()


def cloud_export_crud() -> None:
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
        description="test cloud export",
        plan_id=ID("11467"),
        cloud_provider="azure",
        azure=azure,
    )

    print("### CLOUD EXPORT CREATE")
    created_export = client().cloud_export.create(export)
    pretty_print(created_export)
    print()

    print("### CLOUD EXPORT GET")
    received_export = client().cloud_export.get(created_export.id)
    pretty_print(received_export)
    print()

    print("### CLOUD EXPORT PATCH")
    created_export.description = "PATCHED test cloud export"
    patched_export = client().cloud_export.patch(created_export, "export.description")
    pretty_print(patched_export)
    print()

    print("### CLOUD EXPORT UPDATE")
    created_export.name = "UPDATED community_sdk_python azure cloud export"
    updated_export = client().cloud_export.update(created_export)
    pretty_print(updated_export)
    print()

    print("### CLOUD EXPORT DELETE")
    client().cloud_export.delete(created_export.id)
    print("OK")
    print()


if __name__ == "__main__":
    cloud_exports_list()
    cloud_export_crud()
