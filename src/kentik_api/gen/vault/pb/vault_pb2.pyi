from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class SecretType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SECRET_TYPE_UNSPECIFIED: _ClassVar[SecretType]
    SECRET_TYPE_BASIC_AUTH: _ClassVar[SecretType]
    SECRET_TYPE_SNMP_V1: _ClassVar[SecretType]
    SECRET_TYPE_SNMP_V2C: _ClassVar[SecretType]
    SECRET_TYPE_SNMP_V3: _ClassVar[SecretType]
    SECRET_TYPE_STREAMING_TELEMETRY: _ClassVar[SecretType]
    SECRET_TYPE_BGP_MD5: _ClassVar[SecretType]
    SECRET_TYPE_API_TOKEN: _ClassVar[SecretType]
    SECRET_TYPE_OTHER: _ClassVar[SecretType]

SECRET_TYPE_UNSPECIFIED: SecretType
SECRET_TYPE_BASIC_AUTH: SecretType
SECRET_TYPE_SNMP_V1: SecretType
SECRET_TYPE_SNMP_V2C: SecretType
SECRET_TYPE_SNMP_V3: SecretType
SECRET_TYPE_STREAMING_TELEMETRY: SecretType
SECRET_TYPE_BGP_MD5: SecretType
SECRET_TYPE_API_TOKEN: SecretType
SECRET_TYPE_OTHER: SecretType

class Secret(_message.Message):
    __slots__ = ("name", "value", "version", "description", "type", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    version: int
    description: str
    type: SecretType
    id: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        value: _Optional[str] = ...,
        version: _Optional[int] = ...,
        description: _Optional[str] = ...,
        type: _Optional[_Union[SecretType, str]] = ...,
        id: _Optional[str] = ...,
    ) -> None: ...

class GetSecretRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetSecretResponse(_message.Message):
    __slots__ = ("secret",)
    SECRET_FIELD_NUMBER: _ClassVar[int]
    secret: Secret
    def __init__(self, secret: _Optional[_Union[Secret, _Mapping]] = ...) -> None: ...

class ListSecretRequest(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class ListSecretResponse(_message.Message):
    __slots__ = ("secrets", "invalid_credential_count")
    SECRETS_FIELD_NUMBER: _ClassVar[int]
    INVALID_CREDENTIAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    secrets: _containers.RepeatedCompositeFieldContainer[Secret]
    invalid_credential_count: int
    def __init__(
        self,
        secrets: _Optional[_Iterable[_Union[Secret, _Mapping]]] = ...,
        invalid_credential_count: _Optional[int] = ...,
    ) -> None: ...
