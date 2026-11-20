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

class Role(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ROLE_UNSPECIFIED: _ClassVar[Role]
    ROLE_MEMBER: _ClassVar[Role]
    ROLE_ADMINISTRATOR: _ClassVar[Role]
    ROLE_SUPER_ADMINISTRATOR: _ClassVar[Role]

class LandingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LANDING_TYPE_UNSPECIFIED: _ClassVar[LandingType]
    LANDING_TYPE_LOCAL: _ClassVar[LandingType]
    LANDING_TYPE_OBSERVATION_DECK: _ClassVar[LandingType]
    LANDING_TYPE_NMS_DASHBOARD: _ClassVar[LandingType]
    LANDING_TYPE_NETWORK_EXPLORER: _ClassVar[LandingType]
    LANDING_TYPE_LIBRARY: _ClassVar[LandingType]
    LANDING_TYPE_SYNTHETICS: _ClassVar[LandingType]
    LANDING_TYPE_EXPLORER: _ClassVar[LandingType]
    LANDING_TYPE_ALERTING: _ClassVar[LandingType]
    LANDING_TYPE_INSIGHTS: _ClassVar[LandingType]
    LANDING_TYPE_DASHBOARD: _ClassVar[LandingType]
    LANDING_TYPE_SAVED_VIEW: _ClassVar[LandingType]
    LANDING_TYPE_QUICK_VIEW: _ClassVar[LandingType]
    LANDING_TYPE_MARKET_INTELLIGENCE: _ClassVar[LandingType]
    LANDING_TYPE_AI_ADVISOR: _ClassVar[LandingType]

ROLE_UNSPECIFIED: Role
ROLE_MEMBER: Role
ROLE_ADMINISTRATOR: Role
ROLE_SUPER_ADMINISTRATOR: Role
LANDING_TYPE_UNSPECIFIED: LandingType
LANDING_TYPE_LOCAL: LandingType
LANDING_TYPE_OBSERVATION_DECK: LandingType
LANDING_TYPE_NMS_DASHBOARD: LandingType
LANDING_TYPE_NETWORK_EXPLORER: LandingType
LANDING_TYPE_LIBRARY: LandingType
LANDING_TYPE_SYNTHETICS: LandingType
LANDING_TYPE_EXPLORER: LandingType
LANDING_TYPE_ALERTING: LandingType
LANDING_TYPE_INSIGHTS: LandingType
LANDING_TYPE_DASHBOARD: LandingType
LANDING_TYPE_SAVED_VIEW: LandingType
LANDING_TYPE_QUICK_VIEW: LandingType
LANDING_TYPE_MARKET_INTELLIGENCE: LandingType
LANDING_TYPE_AI_ADVISOR: LandingType

class PermissionEntry(_message.Message):
    __slots__ = ("capability", "allowed")
    CAPABILITY_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_FIELD_NUMBER: _ClassVar[int]
    capability: str
    allowed: bool
    def __init__(
        self, capability: _Optional[str] = ..., allowed: _Optional[bool] = ...
    ) -> None: ...

class User(_message.Message):
    __slots__ = (
        "id",
        "user_email",
        "user_full_name",
        "role",
        "permissions",
        "filter",
        "last_login",
        "cdate",
        "edate",
        "default_landing_page_type",
        "default_landing_page_value",
        "roles",
        "role_sets",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    USER_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    LAST_LOGIN_FIELD_NUMBER: _ClassVar[int]
    CDATE_FIELD_NUMBER: _ClassVar[int]
    EDATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LANDING_PAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_LANDING_PAGE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ROLES_FIELD_NUMBER: _ClassVar[int]
    ROLE_SETS_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_email: str
    user_full_name: str
    role: Role
    permissions: _containers.RepeatedCompositeFieldContainer[PermissionEntry]
    filter: str
    last_login: _timestamp_pb2.Timestamp
    cdate: _timestamp_pb2.Timestamp
    edate: _timestamp_pb2.Timestamp
    default_landing_page_type: LandingType
    default_landing_page_value: str
    roles: _containers.RepeatedScalarFieldContainer[str]
    role_sets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        user_email: _Optional[str] = ...,
        user_full_name: _Optional[str] = ...,
        role: _Optional[_Union[Role, str]] = ...,
        permissions: _Optional[_Iterable[_Union[PermissionEntry, _Mapping]]] = ...,
        filter: _Optional[str] = ...,
        last_login: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        cdate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        edate: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        default_landing_page_type: _Optional[_Union[LandingType, str]] = ...,
        default_landing_page_value: _Optional[str] = ...,
        roles: _Optional[_Iterable[str]] = ...,
        role_sets: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ListUsersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUsersResponse(_message.Message):
    __slots__ = ("users", "invalid_count")
    USERS_FIELD_NUMBER: _ClassVar[int]
    INVALID_COUNT_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[User]
    invalid_count: int
    def __init__(
        self,
        users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...,
        invalid_count: _Optional[int] = ...,
    ) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class CreateUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class CreateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class UpdateUserResponse(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: User
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ...) -> None: ...

class DeleteUserRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteUserResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetApiTokenRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ResetApiTokenResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetActiveSessionsRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ResetActiveSessionsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
