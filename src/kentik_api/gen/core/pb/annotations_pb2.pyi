from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SERVICE_VISIBILITY_PRIVATE: _ClassVar[ServiceVisibility]
    SERVICE_VISIBILITY_PROTECTED: _ClassVar[ServiceVisibility]
    SERVICE_VISIBILITY_INTERNAL: _ClassVar[ServiceVisibility]
    SERVICE_VISIBILITY_PUBLIC: _ClassVar[ServiceVisibility]
    SERVICE_VISIBILITY_PUBLIC_KENTIK: _ClassVar[ServiceVisibility]

class MethodVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    METHOD_VISIBILITY_UNSPECIFIED: _ClassVar[MethodVisibility]
    METHOD_VISIBILITY_PRIVATE: _ClassVar[MethodVisibility]
    METHOD_VISIBILITY_PROTECTED: _ClassVar[MethodVisibility]
    METHOD_VISIBILITY_INTERNAL: _ClassVar[MethodVisibility]
    METHOD_VISIBILITY_PUBLIC: _ClassVar[MethodVisibility]
    METHOD_VISIBILITY_PUBLIC_KENTIK: _ClassVar[MethodVisibility]

SERVICE_VISIBILITY_PRIVATE: ServiceVisibility
SERVICE_VISIBILITY_PROTECTED: ServiceVisibility
SERVICE_VISIBILITY_INTERNAL: ServiceVisibility
SERVICE_VISIBILITY_PUBLIC: ServiceVisibility
SERVICE_VISIBILITY_PUBLIC_KENTIK: ServiceVisibility
METHOD_VISIBILITY_UNSPECIFIED: MethodVisibility
METHOD_VISIBILITY_PRIVATE: MethodVisibility
METHOD_VISIBILITY_PROTECTED: MethodVisibility
METHOD_VISIBILITY_INTERNAL: MethodVisibility
METHOD_VISIBILITY_PUBLIC: MethodVisibility
METHOD_VISIBILITY_PUBLIC_KENTIK: MethodVisibility
SERVICE_SCOPE_FIELD_NUMBER: int
service_scope: _descriptor.FieldDescriptor
PRIVATE_SERVICE_FIELD_NUMBER: int
private_service: _descriptor.FieldDescriptor
VISIBILITY_FIELD_NUMBER: int
visibility: _descriptor.FieldDescriptor
BACKEND_TYPE_FIELD_NUMBER: int
backend_type: _descriptor.FieldDescriptor
AUTHN_FIELD_NUMBER: int
authn: _descriptor.FieldDescriptor
SIGNER_FIELD_NUMBER: int
signer: _descriptor.FieldDescriptor
METHOD_SCOPE_FIELD_NUMBER: int
method_scope: _descriptor.FieldDescriptor
PRIVATE_METHOD_FIELD_NUMBER: int
private_method: _descriptor.FieldDescriptor
METHOD_CATEGORY_FIELD_NUMBER: int
method_category: _descriptor.FieldDescriptor
METHOD_PERMISSION_FIELD_NUMBER: int
method_permission: _descriptor.FieldDescriptor
METHOD_VISIBILITY_FIELD_NUMBER: int
method_visibility: _descriptor.FieldDescriptor
DISPLAY_NAME_FIELD_NUMBER: int
display_name: _descriptor.FieldDescriptor
ENUM_DISPLAY_NAME_FIELD_NUMBER: int
enum_display_name: _descriptor.FieldDescriptor
