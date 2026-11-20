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

DESCRIPTOR: _descriptor.FileDescriptor

class CustomApplication(_message.Message):
    __slots__ = (
        "id",
        "name",
        "description",
        "ip_range",
        "protocol",
        "port",
        "asn",
        "created_date",
        "updated_date",
        "user_id",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IP_RANGE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ASN_FIELD_NUMBER: _ClassVar[int]
    CREATED_DATE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_DATE_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    ip_range: _containers.RepeatedScalarFieldContainer[str]
    protocol: _containers.RepeatedScalarFieldContainer[int]
    port: _containers.RepeatedScalarFieldContainer[int]
    asn: _containers.RepeatedScalarFieldContainer[int]
    created_date: _timestamp_pb2.Timestamp
    updated_date: _timestamp_pb2.Timestamp
    user_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        ip_range: _Optional[_Iterable[str]] = ...,
        protocol: _Optional[_Iterable[int]] = ...,
        port: _Optional[_Iterable[int]] = ...,
        asn: _Optional[_Iterable[int]] = ...,
        created_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        updated_date: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        user_id: _Optional[str] = ...,
    ) -> None: ...

class ListCustomApplicationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListCustomApplicationsResponse(_message.Message):
    __slots__ = ("applications",)
    APPLICATIONS_FIELD_NUMBER: _ClassVar[int]
    applications: _containers.RepeatedCompositeFieldContainer[CustomApplication]
    def __init__(
        self,
        applications: _Optional[_Iterable[_Union[CustomApplication, _Mapping]]] = ...,
    ) -> None: ...

class GetCustomApplicationRequest(_message.Message):
    __slots__ = ("custom_application_id",)
    CUSTOM_APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    custom_application_id: str
    def __init__(self, custom_application_id: _Optional[str] = ...) -> None: ...

class GetCustomApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: CustomApplication
    def __init__(
        self, application: _Optional[_Union[CustomApplication, _Mapping]] = ...
    ) -> None: ...

class CreateCustomApplicationRequest(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: CustomApplication
    def __init__(
        self, application: _Optional[_Union[CustomApplication, _Mapping]] = ...
    ) -> None: ...

class CreateCustomApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: CustomApplication
    def __init__(
        self, application: _Optional[_Union[CustomApplication, _Mapping]] = ...
    ) -> None: ...

class UpdateCustomApplicationRequest(_message.Message):
    __slots__ = ("custom_application_id", "application")
    CUSTOM_APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    custom_application_id: str
    application: CustomApplication
    def __init__(
        self,
        custom_application_id: _Optional[str] = ...,
        application: _Optional[_Union[CustomApplication, _Mapping]] = ...,
    ) -> None: ...

class UpdateCustomApplicationResponse(_message.Message):
    __slots__ = ("application",)
    APPLICATION_FIELD_NUMBER: _ClassVar[int]
    application: CustomApplication
    def __init__(
        self, application: _Optional[_Union[CustomApplication, _Mapping]] = ...
    ) -> None: ...

class DeleteCustomApplicationRequest(_message.Message):
    __slots__ = ("custom_application_id",)
    CUSTOM_APPLICATION_ID_FIELD_NUMBER: _ClassVar[int]
    custom_application_id: str
    def __init__(self, custom_application_id: _Optional[str] = ...) -> None: ...

class DeleteCustomApplicationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
