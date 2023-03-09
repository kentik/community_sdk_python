import os
from copy import deepcopy
from typing import Optional, Union
from urllib.parse import urlparse

from kentik_api import KentikAPI
from kentik_api.cloudexport.cloud_export import (
    AwsProperties,
    AzureProperties,
    CloudExport,
    CloudExportType,
    GceProperties,
    IbmProperties,
    Status,
)
from kentik_api.public.types import ID
from kentik_api.utils import get_credentials, get_url

required_env_variables = ("KTAPI_AUTH_EMAIL", "KTAPI_AUTH_TOKEN", "KTAPI_PLAN_ID")
credentials_missing_str = (
    f"Following environment variables must be set in order to run the test: {', '.join(required_env_variables)}"
)
credentials_present = all(v in os.environ for v in required_env_variables)


def client() -> KentikAPI:
    """Create KentikAPI client"""

    email, token = get_credentials(profile="")
    url = get_url()
    if url:
        api_host = urlparse(url).netloc
        if not api_host:
            api_host = urlparse(url).path
    else:
        api_host = None
    return KentikAPI(email, token, api_host=api_host)


def clear_readonly_fields(e: CloudExport) -> CloudExport:
    result = deepcopy(e)  # so we don't modify the source cloud export
    result._api_root = ""
    result._flow_dest = ""
    result._current_status = Status()
    return result


def execute_cloud_export_crud_steps(
    ce: CloudExport,
    update_settings: Union[AwsProperties, AzureProperties, GceProperties, IbmProperties],
) -> None:
    api = client()
    created: Optional[CloudExport] = None
    try:
        # create
        ce.plan_id = ID(os.environ["KTAPI_PLAN_ID"])
        created = api.cloud_export.create(ce)
        assert isinstance(created, CloudExport)
        assert created.id != ID()
        assert created.type == ce.type
        assert created.enabled == ce.enabled
        assert created.name == ce.name
        assert created.description == ce.description
        assert created.plan_id == ce.plan_id
        assert created.cloud_provider == ce.cloud_provider
        assert getattr(created, created.cloud_provider.value) == getattr(ce, ce.cloud_provider.value)

        # read
        received = api.cloud_export.get(created.id)
        assert clear_readonly_fields(received) == clear_readonly_fields(created)

        # update
        received.type = CloudExportType.KENTIK_MANAGED
        received.enabled = False
        received.name += "-updated"
        received.description += " updated"
        setattr(received, received.cloud_provider.value, update_settings)
        updated = api.cloud_export.update(received)
        assert clear_readonly_fields(updated) == clear_readonly_fields(received)

    finally:
        if created:
            # delete (even if assertion failed)
            api.cloud_export.delete(created.id)
