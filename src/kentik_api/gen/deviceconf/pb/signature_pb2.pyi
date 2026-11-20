from typing import ClassVar as _ClassVar
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class SignatureAlgorithm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNATURE_ALGORITHM_UNSPECIFIED: _ClassVar[SignatureAlgorithm]
    SIGNATURE_ALGORITHM_ECDSA_SHA256: _ClassVar[SignatureAlgorithm]

SIGNATURE_ALGORITHM_UNSPECIFIED: SignatureAlgorithm
SIGNATURE_ALGORITHM_ECDSA_SHA256: SignatureAlgorithm

class MessageSignature(_message.Message):
    __slots__ = ("signer_id", "algorithm", "signature")
    SIGNER_ID_FIELD_NUMBER: _ClassVar[int]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    signer_id: str
    algorithm: SignatureAlgorithm
    signature: bytes
    def __init__(
        self,
        signer_id: _Optional[str] = ...,
        algorithm: _Optional[_Union[SignatureAlgorithm, str]] = ...,
        signature: _Optional[bytes] = ...,
    ) -> None: ...
