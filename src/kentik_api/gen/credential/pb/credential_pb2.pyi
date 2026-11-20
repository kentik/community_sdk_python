import datetime
from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class CredentialType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREDENTIAL_TYPE_UNSPECIFIED: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_BASIC_AUTH: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_SNMP_V1: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_SNMP_V2C: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_SNMP_V3: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_STREAMING_TELEMETRY: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_BGP_MD5: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_API_TOKEN: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_OTHER: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_SSH_KEY: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_SSH_PASSWORD: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_AI_API_TOKEN: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_MCP_HTTP_HEADERS: _ClassVar[CredentialType]
    CREDENTIAL_TYPE_CLOUD: _ClassVar[CredentialType]

CREDENTIAL_TYPE_UNSPECIFIED: CredentialType
CREDENTIAL_TYPE_BASIC_AUTH: CredentialType
CREDENTIAL_TYPE_SNMP_V1: CredentialType
CREDENTIAL_TYPE_SNMP_V2C: CredentialType
CREDENTIAL_TYPE_SNMP_V3: CredentialType
CREDENTIAL_TYPE_STREAMING_TELEMETRY: CredentialType
CREDENTIAL_TYPE_BGP_MD5: CredentialType
CREDENTIAL_TYPE_API_TOKEN: CredentialType
CREDENTIAL_TYPE_OTHER: CredentialType
CREDENTIAL_TYPE_SSH_KEY: CredentialType
CREDENTIAL_TYPE_SSH_PASSWORD: CredentialType
CREDENTIAL_TYPE_AI_API_TOKEN: CredentialType
CREDENTIAL_TYPE_MCP_HTTP_HEADERS: CredentialType
CREDENTIAL_TYPE_CLOUD: CredentialType

class CreatedBy(_message.Message):
    __slots__ = ("id", "email", "full_name")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    full_name: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        email: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
    ) -> None: ...

class Consumer(_message.Message):
    __slots__ = ("type", "consumer_id")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_ID_FIELD_NUMBER: _ClassVar[int]
    type: str
    consumer_id: str
    def __init__(
        self, type: _Optional[str] = ..., consumer_id: _Optional[str] = ...
    ) -> None: ...

class Credential(_message.Message):
    __slots__ = (
        "id",
        "name",
        "version",
        "description",
        "type",
        "cdate",
        "edate",
        "created_by",
        "labels",
        "consumers",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    CONSUMERS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: int
    description: str
    type: CredentialType
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    created_by: CreatedBy
    labels: _containers.RepeatedScalarFieldContainer[str]
    consumers: _containers.RepeatedCompositeFieldContainer[Consumer]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        description: _Optional[str] = ...,
        type: _Optional[_Union[CredentialType, str]] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        created_by: _Optional[_Union[CreatedBy, _Mapping]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
        consumers: _Optional[_Iterable[_Union[Consumer, _Mapping]]] = ...,
    ) -> None: ...

class CredentialGroup(_message.Message):
    __slots__ = (
        "id",
        "name",
        "version",
        "description",
        "type",
        "cdate",
        "edate",
        "created_by",
        "labels",
        "consumers",
        "credentials",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    CONSUMERS_FIELD_NUMBER: _ClassVar[int]
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: int
    description: str
    type: CredentialType
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    created_by: CreatedBy
    labels: _containers.RepeatedScalarFieldContainer[str]
    consumers: _containers.RepeatedCompositeFieldContainer[Consumer]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        description: _Optional[str] = ...,
        type: _Optional[_Union[CredentialType, str]] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        created_by: _Optional[_Union[CreatedBy, _Mapping]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
        consumers: _Optional[_Iterable[_Union[Consumer, _Mapping]]] = ...,
        credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ...,
    ) -> None: ...

class CredentialOverview(_message.Message):
    __slots__ = ("name", "type")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: CredentialType
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[CredentialType, str]] = ...,
    ) -> None: ...

class Token(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    def __init__(
        self, key: _Optional[str] = ..., value: _Optional[str] = ...
    ) -> None: ...

class ListCredentialsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCredentialsResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    def __init__(
        self, credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ...
    ) -> None: ...

class ListCredentialGroupsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCredentialGroupsResponse(_message.Message):
    __slots__ = ("groups",)
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    groups: _containers.RepeatedCompositeFieldContainer[CredentialGroup]
    def __init__(
        self, groups: _Optional[_Iterable[_Union[CredentialGroup, _Mapping]]] = ...
    ) -> None: ...

class ListCredentialOverviewsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCredentialOverviewsResponse(_message.Message):
    __slots__ = ("overviews",)
    OVERVIEWS_FIELD_NUMBER: _ClassVar[int]
    overviews: _containers.RepeatedCompositeFieldContainer[CredentialOverview]
    def __init__(
        self,
        overviews: _Optional[_Iterable[_Union[CredentialOverview, _Mapping]]] = ...,
    ) -> None: ...

class GetCredentialGroupRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetCredentialGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: CredentialGroup
    def __init__(
        self, group: _Optional[_Union[CredentialGroup, _Mapping]] = ...
    ) -> None: ...

class GetCredentialRequest(_message.Message):
    __slots__ = ("name", "version", "all_versions")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ALL_VERSIONS_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: int
    all_versions: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        version: _Optional[int] = ...,
        all_versions: _Optional[bool] = ...,
    ) -> None: ...

class GetCredentialResponse(_message.Message):
    __slots__ = ("credentials",)
    CREDENTIALS_FIELD_NUMBER: _ClassVar[int]
    credentials: _containers.RepeatedCompositeFieldContainer[Credential]
    def __init__(
        self, credentials: _Optional[_Iterable[_Union[Credential, _Mapping]]] = ...
    ) -> None: ...

class CreateCredentialGroupRequest(_message.Message):
    __slots__ = ("name", "type", "description", "tokens", "labels")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: CredentialType
    description: str
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[CredentialType, str]] = ...,
        description: _Optional[str] = ...,
        tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class CreateCredentialGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: CredentialGroup
    def __init__(
        self, group: _Optional[_Union[CredentialGroup, _Mapping]] = ...
    ) -> None: ...

class UpdateCredentialGroupRequest(_message.Message):
    __slots__ = ("name", "type", "description", "tokens", "labels")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: CredentialType
    description: str
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    labels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[CredentialType, str]] = ...,
        description: _Optional[str] = ...,
        tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...,
        labels: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpdateCredentialGroupResponse(_message.Message):
    __slots__ = ("group",)
    GROUP_FIELD_NUMBER: _ClassVar[int]
    group: CredentialGroup
    def __init__(
        self, group: _Optional[_Union[CredentialGroup, _Mapping]] = ...
    ) -> None: ...

class DeleteCredentialGroupRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class DeleteCredentialGroupResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteCredentialRequest(_message.Message):
    __slots__ = ("name", "version")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: int
    def __init__(
        self, name: _Optional[str] = ..., version: _Optional[int] = ...
    ) -> None: ...

class DeleteCredentialResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AssignConsumerRequest(_message.Message):
    __slots__ = ("name", "consumer")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONSUMER_FIELD_NUMBER: _ClassVar[int]
    name: str
    consumer: Consumer
    def __init__(
        self,
        name: _Optional[str] = ...,
        consumer: _Optional[_Union[Consumer, _Mapping]] = ...,
    ) -> None: ...

class AssignConsumerResponse(_message.Message):
    __slots__ = ("credential",)
    CREDENTIAL_FIELD_NUMBER: _ClassVar[int]
    credential: Credential
    def __init__(
        self, credential: _Optional[_Union[Credential, _Mapping]] = ...
    ) -> None: ...
