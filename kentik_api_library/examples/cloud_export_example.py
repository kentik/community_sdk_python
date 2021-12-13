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
        location="location",
        resource_group="resource_group",
        storage_account="storage_account",
        subscription_id=ID("1234"),
        security_principal_enabled=True,
    )
    export = CloudExport(
        name="community_sdk_python azure cloud export",
        type=CloudExportType.CLOUD_EXPORT_TYPE_KENTIK_MANAGED,
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
    created_export.name = "PATCHED community_sdk_python azure cloud export"
    patched_export = client().cloud_export.patch(created_export, "export.name")
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
