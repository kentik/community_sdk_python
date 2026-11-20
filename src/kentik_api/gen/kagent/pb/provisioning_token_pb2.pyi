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

class ProvisioningToken(_message.Message):
    __slots__ = (
        "token",
        "name",
        "max_usage_count",
        "current_usage_count",
        "expires_at",
        "allowed_private_cidrs",
        "allowed_public_cidrs",
        "cluster_id",
        "requires_approval",
        "config",
        "revoked",
        "created_by",
        "ctime",
        "utime",
    )
    class AgentConfig(_message.Message):
        __slots__ = ("site_id",)
        SITE_ID_FIELD_NUMBER: _ClassVar[int]
        site_id: str
        def __init__(self, site_id: _Optional[str] = ...) -> None: ...

    TOKEN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_USAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_USAGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PRIVATE_CIDRS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_PUBLIC_CIDRS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_APPROVAL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    REVOKED_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    UTIME_FIELD_NUMBER: _ClassVar[int]
    token: str
    name: str
    max_usage_count: int
    current_usage_count: int
    expires_at: _timestamp_pb2.Timestamp
    allowed_private_cidrs: _containers.RepeatedScalarFieldContainer[str]
    allowed_public_cidrs: _containers.RepeatedScalarFieldContainer[str]
    cluster_id: str
    requires_approval: bool
    config: ProvisioningToken.AgentConfig
    revoked: TokenRevoked
    created_by: str
    ctime: _timestamp_pb2.Timestamp
    utime: _timestamp_pb2.Timestamp
    def __init__(
        self,
        token: _Optional[str] = ...,
        name: _Optional[str] = ...,
        max_usage_count: _Optional[int] = ...,
        current_usage_count: _Optional[int] = ...,
        expires_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        allowed_private_cidrs: _Optional[_Iterable[str]] = ...,
        allowed_public_cidrs: _Optional[_Iterable[str]] = ...,
        cluster_id: _Optional[str] = ...,
        requires_approval: _Optional[bool] = ...,
        config: _Optional[_Union[ProvisioningToken.AgentConfig, _Mapping]] = ...,
        revoked: _Optional[_Union[TokenRevoked, _Mapping]] = ...,
        created_by: _Optional[str] = ...,
        ctime: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
        utime: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class TokenRevoked(_message.Message):
    __slots__ = ("revoked_by", "revoked_at")
    REVOKED_BY_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    revoked_by: str
    revoked_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        revoked_by: _Optional[str] = ...,
        revoked_at: _Optional[
            _Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]
        ] = ...,
    ) -> None: ...

class CreateProvisioningTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: ProvisioningToken
    def __init__(
        self, token: _Optional[_Union[ProvisioningToken, _Mapping]] = ...
    ) -> None: ...

class CreateProvisioningTokenResponse(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: ProvisioningToken
    def __init__(
        self, token: _Optional[_Union[ProvisioningToken, _Mapping]] = ...
    ) -> None: ...

class ListProvisioningTokensRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListProvisioningTokensResponse(_message.Message):
    __slots__ = ("tokens",)
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[ProvisioningToken]
    def __init__(
        self, tokens: _Optional[_Iterable[_Union[ProvisioningToken, _Mapping]]] = ...
    ) -> None: ...

class GetProvisioningTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class GetProvisioningTokenResponse(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: ProvisioningToken
    def __init__(
        self, token: _Optional[_Union[ProvisioningToken, _Mapping]] = ...
    ) -> None: ...

class RevokeProvisioningTokenRequest(_message.Message):
    __slots__ = ("token", "revoked_by")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    REVOKED_BY_FIELD_NUMBER: _ClassVar[int]
    token: str
    revoked_by: str
    def __init__(
        self, token: _Optional[str] = ..., revoked_by: _Optional[str] = ...
    ) -> None: ...

class RevokeProvisioningTokenResponse(_message.Message):
    __slots__ = ("revoked",)
    REVOKED_FIELD_NUMBER: _ClassVar[int]
    revoked: TokenRevoked
    def __init__(
        self, revoked: _Optional[_Union[TokenRevoked, _Mapping]] = ...
    ) -> None: ...

class ListAgentsByProvisioningTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class ListAgentsByProvisioningTokenResponse(_message.Message):
    __slots__ = ("agents",)
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, agents: _Optional[_Iterable[str]] = ...) -> None: ...
