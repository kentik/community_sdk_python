from typing import ClassVar as _ClassVar
from typing import Optional as _Optional

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceNowConfig(_message.Message):
    __slots__ = (
        "id",
        "company_id",
        "name",
        "description",
        "device_staging_table_name",
        "push_frequency_seconds",
        "proxy_agent_id",
        "credential_vault_name",
        "enabled",
        "api_url",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    DEVICE_STAGING_TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    PUSH_FREQUENCY_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROXY_AGENT_ID_FIELD_NUMBER: _ClassVar[int]
    CREDENTIAL_VAULT_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    API_URL_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    name: str
    description: str
    device_staging_table_name: str
    push_frequency_seconds: int
    proxy_agent_id: str
    credential_vault_name: str
    enabled: bool
    api_url: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        company_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        device_staging_table_name: _Optional[str] = ...,
        push_frequency_seconds: _Optional[int] = ...,
        proxy_agent_id: _Optional[str] = ...,
        credential_vault_name: _Optional[str] = ...,
        enabled: _Optional[bool] = ...,
        api_url: _Optional[str] = ...,
    ) -> None: ...
