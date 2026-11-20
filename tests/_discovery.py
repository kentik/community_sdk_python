# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Shared schema/wrapper discovery helpers for the tests/ tree.

Every operation, parameter, and declared response status code exercised by
the generated/e2e test suites is discovered from the generated code itself
(AST-parsed or introspected at runtime) rather than hand-listed, so new
services/endpoints picked up by `uv run poe generate` are covered automatically.

Lives at the tests/ root (not inside tests/generated/) because both
tests/generated/*.py and tests/e2e/*.py import it; tests/conftest.py puts
tests/ on sys.path so `import _discovery` resolves the same way regardless
of which subdirectory pytest is invoked against.
"""

from __future__ import annotations

import ast
import functools
import importlib
import inspect
import json
import pkgutil
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Union, get_args, get_origin

from google.api import visibility_pb2
from google.protobuf import message_factory
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.json_format import ParseDict
from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from kentik_api.core.api_config import APIConfig
from scripts.generation._shared import iter_service_dirs, service_to_pascal_case


@dataclass(frozen=True)
class WrapperCase:
    module_path: str
    file_path: Path
    wrapper_class: str
    method_name: str
    rest_module_alias: str
    rest_function_name: str


def case_label(case: WrapperCase) -> str:
    return (
        f"{case.wrapper_class}.{case.method_name} "
        f"[{case.module_path}:{case.rest_module_alias}.{case.rest_function_name}]"
    )


def print_case_start(case: WrapperCase, mode: str) -> None:
    print(f'Testing against "{case_label(case)}". Mode={mode}. START')


def print_case_result(case: WrapperCase, mode: str, result: str) -> None:
    print(f'Testing against "{case_label(case)}". Mode={mode}. RESULT={result}')


def generated_root() -> Path:
    return Path(__file__).resolve().parents[1] / "src" / "kentik_api" / "gen"


@functools.cache
def _recorded_routes() -> dict[tuple[str, str], str | None]:
    surface = json.loads(
        (Path(__file__).resolve().parents[1] / "api_surface.json").read_text("utf-8")
    )
    return {
        (service, operation["method"]): operation.get("grpc")
        for service, record in surface["services"].items()
        for operation in record["operations"].values()
    }


def recorded_grpc_route(case: WrapperCase) -> str | None:
    """The RPC api_surface.json records for this method; None means REST only.

    Losing a route is a breaking change in that record, so a method may raise
    NotImplementedError on gRPC only where the record says it has no route.
    """
    service = case.module_path.split(".")[2]
    return _recorded_routes()[(service, case.method_name)]


def _parse_wrapper_calls(file_path: Path) -> dict[str, tuple[str, str]]:
    tree = ast.parse(file_path.read_text(encoding="utf-8"))

    wrapper_class = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name.endswith("ServiceWrapper"):
            wrapper_class = node
            break

    if wrapper_class is None:
        return {}

    mapping: dict[str, tuple[str, str]] = {}
    for node in wrapper_class.body:
        if not isinstance(node, ast.FunctionDef) or node.name in {"__init__"}:
            continue

        alias = None
        rest_func = None
        for sub in ast.walk(node):
            if not isinstance(sub, ast.Return) or not isinstance(sub.value, ast.Call):
                continue
            call_func = sub.value.func
            if (
                isinstance(call_func, ast.Attribute)
                and isinstance(call_func.value, ast.Name)
                and call_func.value.id.startswith("Rest")
            ):
                alias = call_func.value.id
                rest_func = call_func.attr
                break

        if alias and rest_func:
            mapping[node.name] = (alias, rest_func)

    return mapping


def discover_cases() -> list[WrapperCase]:
    cases: list[WrapperCase] = []

    for service_dir in iter_service_dirs(generated_root()):
        service = service_dir.name
        services_dir = service_dir / "services"
        if not services_dir.exists():
            services_dir = service_dir / "service"
            if not services_dir.exists():
                continue

        wrapper_file = services_dir / f"{service}.py"
        if not wrapper_file.exists():
            continue

        method_map = _parse_wrapper_calls(wrapper_file)
        wrapper_class = f"{service_to_pascal_case(service)}ServiceWrapper"
        module_path = f"kentik_api.gen.{service}.{services_dir.name}.{service}"

        for method_name, (alias, fn_name) in sorted(method_map.items()):
            cases.append(
                WrapperCase(
                    module_path=module_path,
                    file_path=wrapper_file,
                    wrapper_class=wrapper_class,
                    method_name=method_name,
                    rest_module_alias=alias,
                    rest_function_name=fn_name,
                )
            )

    return cases


_NUMERIC_ID_NAMES = frozenset(
    {"id", "tagid", "deviceid", "customdimensionid", "populatorid"}
)
_NUMERIC_COUNT_NAMES = frozenset({"offset", "limit", "page", "size"})
_SAMPLE_TIMESTAMP = "2024-01-01T00:00:00Z"


def sample_value_by_name(name: str) -> Any:
    lowered = name.lower()
    if lowered in _NUMERIC_ID_NAMES:
        return "1"
    if lowered.endswith("time"):
        return _SAMPLE_TIMESTAMP
    if lowered.endswith("name"):
        return "name"
    if lowered.startswith(("is", "has")):
        return True
    if lowered in _NUMERIC_COUNT_NAMES:
        return 1
    return object()


class _RecursiveModel(ValueError):
    pass


def sample_model_instance(
    model_cls: type[BaseModel],
    _seen: frozenset = frozenset(),
    every_field: bool = False,
) -> BaseModel:
    """Builds a valid instance of a generated Pydantic model.

    By default only required fields are filled, the smallest payload a real
    caller could send. every_field also fills each optional field, except one
    that would recurse into a model already being sampled.
    """
    if model_cls in _seen:
        raise _RecursiveModel(
            f"Recursive model reference detected while sampling {model_cls!r}"
        )
    seen = _seen | {model_cls}

    kwargs: dict[str, Any] = {}
    for field_name, field_info in model_cls.model_fields.items():
        if field_info.is_required():
            kwargs[field_name] = _sample_value_for_type(
                field_info.annotation, field_name, seen, every_field
            )
        elif every_field:
            try:
                kwargs[field_name] = _sample_value_for_type(
                    field_info.annotation, field_name, seen, every_field
                )
            except _RecursiveModel:
                pass
    return model_cls(**kwargs)


def _sample_value_for_type(
    annotation: Any, name: str, seen: frozenset, every_field: bool = False
) -> Any:
    if annotation is inspect.Parameter.empty:
        return sample_value_by_name(name)
    if annotation is Any:
        value = sample_value_by_name(name)
        return f"{name}_value" if type(value) is object else value

    origin = get_origin(annotation)
    if origin is Union:
        args = [arg for arg in get_args(annotation) if arg is not type(None)]
        return (
            _sample_value_for_type(args[0], name, seen, every_field) if args else None
        )

    if origin in (list, set, frozenset):
        args = get_args(annotation)
        item_type = args[0] if args else Any
        item = _sample_value_for_type(item_type, name, seen, every_field)
        return [item] if origin is list else {item}

    if origin is dict:
        return {}

    if annotation is APIConfig:
        return APIConfig(
            base_path="https://api.example.com",
            auth_email="override@example.com",
            auth_token="override-token",
        )

    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return sample_model_instance(annotation, seen, every_field)

    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return next(iter(annotation))

    if annotation is str:
        lowered = name.lower()
        if lowered in _NUMERIC_ID_NAMES or lowered in _NUMERIC_COUNT_NAMES:
            return "1"
        if lowered.endswith("time"):
            return _SAMPLE_TIMESTAMP
        return f"{name}_value"
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is bool:
        return True
    if annotation is bytes:
        return b"sample-bytes"

    return sample_value_by_name(name)


def proto_field(message_descriptor: Any, field_path: str) -> Any:
    """Resolves a dotted request field path as ParseDict does: by name or JSON name."""
    field = None
    for segment in field_path.split("."):
        if message_descriptor is None:
            return None
        field = message_descriptor.fields_by_name.get(segment) or next(
            (f for f in message_descriptor.fields if f.json_name == segment), None
        )
        if field is None:
            return None
        message_descriptor = field.message_type
    return field


_PROTO_INT_TYPES = frozenset(
    {
        FieldDescriptor.CPPTYPE_INT32,
        FieldDescriptor.CPPTYPE_INT64,
        FieldDescriptor.CPPTYPE_UINT32,
        FieldDescriptor.CPPTYPE_UINT64,
    }
)


def proto_sample_value(field: Any, value: Any) -> Any:
    """Swaps a sample the proto field rejects for one it accepts.

    REST signatures type enum, int64, and Timestamp query parameters as `str`,
    so a sample such as "view_value" is fine for REST but fails ParseDict on
    gRPC.
    """
    if isinstance(value, list):
        return [proto_sample_value(field, item) for item in value]
    if field.enum_type is not None and value not in field.enum_type.values_by_name:
        values = field.enum_type.values
        return next((v.name for v in values if v.number != 0), values[0].name)
    message_type = field.message_type
    if (
        message_type is not None
        and message_type.full_name == "google.protobuf.Timestamp"
    ):
        try:
            Timestamp().FromJsonString(value)
        except (TypeError, ValueError):
            return _SAMPLE_TIMESTAMP
    elif message_type is not None and message_type.full_name in _WELL_KNOWN_SAMPLES:
        return _WELL_KNOWN_SAMPLES[message_type.full_name]
    if field.cpp_type in _PROTO_INT_TYPES:
        try:
            int(value)
        except (TypeError, ValueError):
            return "1"
    return value


_WELL_KNOWN_SAMPLES = {
    "google.protobuf.Timestamp": _SAMPLE_TIMESTAMP,
    "google.protobuf.Duration": "1s",
    "google.protobuf.FieldMask": "id",
    "google.protobuf.Struct": {"key": "value"},
    "google.protobuf.Value": "value",
    "google.protobuf.ListValue": ["value"],
    "google.protobuf.Any": {
        "@type": "type.googleapis.com/google.protobuf.Timestamp",
        "value": _SAMPLE_TIMESTAMP,
    },
}


def proto_sample_body(descriptor: Any, body: Any) -> Any:
    """Swaps each body sample the request message rejects for one it accepts.

    Each enum gets a non-zero value, so a sent field is never at its default,
    and each oneof keeps only its first member. A key that names no field is
    kept, so the real ParseDict still fails on it.
    """
    if not isinstance(body, dict):
        return body
    adapted: dict[str, Any] = {}
    oneofs_seen: set[str] = set()
    for key, value in body.items():
        field = proto_field(descriptor, key)
        if field is None or value is None:
            adapted[key] = value
            continue
        oneof = field.containing_oneof
        if oneof is not None and not oneof.name.startswith("_"):
            if oneof.name in oneofs_seen:
                continue
            oneofs_seen.add(oneof.name)
        adapted[key] = _proto_sample_field(field, value)
    return adapted


def _proto_sample_field(field: Any, value: Any) -> Any:
    message_type = field.message_type
    if message_type is not None and message_type.GetOptions().map_entry:
        return value
    if isinstance(value, list):
        return [_proto_sample_item(field, item) for item in value]
    return _proto_sample_item(field, value)


def _proto_sample_item(field: Any, value: Any) -> Any:
    message_type = field.message_type
    if message_type is None:
        if field.enum_type is not None:
            zero = field.enum_type.values_by_number.get(0)
            if zero is not None and value == zero.name:
                value = None  # proto_sample_value then picks a non-zero name
        return proto_sample_value(field, value)
    if message_type.full_name in _WELL_KNOWN_SAMPLES:
        return proto_sample_value(field, value)
    if message_type.full_name.startswith("google.protobuf."):
        return proto_sample_value(message_type.fields_by_name["value"], value)
    return proto_sample_body(message_type, value)


@functools.cache
def _proto_services(service: str) -> dict[str, Any]:
    """Maps each proto service name in a Service's pb package to its descriptor."""
    package = importlib.import_module(f"kentik_api.gen.{service}.pb")
    services: dict[str, Any] = {}
    for module in pkgutil.iter_modules(package.__path__):
        if module.name.endswith("_pb2"):
            descriptor = importlib.import_module(
                f"{package.__name__}.{module.name}"
            ).DESCRIPTOR
            services.update(descriptor.services_by_name)
    return services


def sample_grpc_response(case: WrapperCase) -> Any:
    """A response message for the method's recorded RPC with every field set.

    Built from the proto descriptor, not from the SDK's models, so a model whose
    field type or name disagrees with the wire fails to parse or round-trip.
    Each oneof gets its first member, and a message type already on the path is
    left unset so recursion ends.
    """
    service_name, rpc = (recorded_grpc_route(case) or "").split("/")
    service = case.module_path.split(".")[2]
    output = _proto_services(service)[service_name].methods_by_name[rpc].output_type
    message_cls = message_factory.GetMessageClass(output)
    return ParseDict(_filled_message(output, frozenset()), message_cls())


def _filled_message(descriptor: Any, seen: frozenset) -> dict[str, Any]:
    seen = seen | {descriptor.full_name}
    filled: dict[str, Any] = {}
    oneofs_seen: set[str] = set()
    for field in descriptor.fields:
        if _is_internal(field):
            continue
        oneof = field.containing_oneof
        if oneof is not None and not oneof.name.startswith("_"):
            if oneof.name in oneofs_seen:
                continue
            oneofs_seen.add(oneof.name)
        value = _filled_value(field, seen)
        if value is None:
            continue
        message_type = field.message_type
        is_map = message_type is not None and message_type.GetOptions().map_entry
        filled[field.json_name] = [value] if field.is_repeated and not is_map else value
    return filled


def _is_internal(field: Any) -> bool:
    """Upstream keeps an INTERNAL field out of the published schema, and so the SDK."""
    options = field.GetOptions()
    return (
        options.HasExtension(visibility_pb2.field_visibility)
        and options.Extensions[visibility_pb2.field_visibility].restriction
        == "INTERNAL"
    )


def _filled_value(field: Any, seen: frozenset) -> Any:
    message_type = field.message_type
    if message_type is not None:
        if message_type.GetOptions().map_entry:
            value = _filled_value(message_type.fields_by_name["value"], seen)
            key = _filled_value(message_type.fields_by_name["key"], seen)
            return None if value is None else {str(key).lower(): value}
        if message_type.full_name in _WELL_KNOWN_SAMPLES:
            return _WELL_KNOWN_SAMPLES[message_type.full_name]
        if message_type.full_name.startswith("google.protobuf."):
            return _filled_value(message_type.fields_by_name["value"], seen)
        if message_type.full_name in seen:
            return None
        return _filled_message(message_type, seen)
    if field.enum_type is not None:
        values = field.enum_type.values
        return next((v.name for v in values if v.number != 0), values[0].name)
    if field.type == FieldDescriptor.TYPE_BOOL:
        return True
    if field.type == FieldDescriptor.TYPE_STRING:
        return f"{field.name}-value"
    if field.type == FieldDescriptor.TYPE_BYTES:
        return "Ynl0ZXM="
    if field.cpp_type in (
        FieldDescriptor.CPPTYPE_DOUBLE,
        FieldDescriptor.CPPTYPE_FLOAT,
    ):
        return 1.5
    return "7" if field.cpp_type in _PROTO_INT_TYPES else 7


def sample_value_for_annotation(
    annotation: Any, name: str, every_field: bool = False
) -> Any:
    if annotation is inspect.Parameter.empty:
        return sample_value_by_name(name)
    return _sample_value_for_type(annotation, name, frozenset(), every_field)


def sample_rest_response(method: Any) -> Any:
    """A success body built from the method's return type, every field set.

    For an operation with no gRPC route, such as one from the local schema
    base, where no proto message exists to sample from.
    """
    annotation = inspect.signature(method).return_annotation
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return sample_model_instance(annotation, every_field=True).model_dump(
            mode="json", by_alias=True, exclude_none=True
        )
    return _sample_value_for_type(annotation, "response", frozenset(), True)


def build_required_kwargs(method: Any) -> dict[str, Any]:
    sig = inspect.signature(method)
    kwargs: dict[str, Any] = {}
    for param in sig.parameters.values():
        if param.name == "self":
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        if param.default is inspect.Parameter.empty:
            kwargs[param.name] = sample_value_for_annotation(
                param.annotation, param.name
            )
    return kwargs


def build_all_kwargs(method: Any, every_field: bool = True) -> dict[str, Any]:
    """Like `build_required_kwargs`, but also fills optional parameters.

    This exercises every declared option (required and optional) on an
    operation, not just the minimum needed to make a valid call. every_field
    also fills every optional field of a request body.
    """
    sig = inspect.signature(method)
    kwargs: dict[str, Any] = {}
    for param in sig.parameters.values():
        if param.name == "self":
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        kwargs[param.name] = sample_value_for_annotation(
            param.annotation, param.name, every_field
        )
    return kwargs


@dataclass(frozen=True)
class RestCallMetadata:
    method: str
    path: str
    expected_status: int
    error_cls_name: str
    operation_name: str


def parse_rest_call_metadata(
    rest_module: Any, function_name: str
) -> RestCallMetadata | None:
    """Reads the `request_json(...)` call inside a generated REST function."""
    from scripts.generation._shared import parse_generated_rest_module

    file_path = Path(inspect.getfile(rest_module))
    for op in parse_generated_rest_module(file_path):
        if op.name == function_name:
            return RestCallMetadata(
                method=op.http_method,
                path=op.path,
                expected_status=op.expected_status,
                error_cls_name=op.error_cls_name,
                operation_name=op.operation_name,
            )
    return None


def error_module_for(rest_module: Any):
    """Imports the `error` package generated alongside a service's REST module."""
    parts = rest_module.__name__.split(".")
    service_pkg = ".".join(parts[:-2])
    return importlib.import_module(f"{service_pkg}.error")


@dataclass(frozen=True)
class EndpointCase:
    wrapper: WrapperCase
    operation_name: str
    method: str
    path: str


def discover_endpoint_cases() -> list[EndpointCase]:
    """Pairs every discovered wrapper case with its REST method/operation name.

    Shared by tests/e2e/test_endpoints_e2e.py and
    tests/e2e/test_endpoints_e2e_grpc.py: gRPC coverage rides on the same
    underlying REST operations, so both suites need the identical
    GET-vs-mutating classification rather than deriving it twice.
    """
    cases: list[EndpointCase] = []
    for wrapper_case in discover_cases():
        module = importlib.import_module(wrapper_case.module_path)
        rest_module = getattr(module, wrapper_case.rest_module_alias)
        metadata = parse_rest_call_metadata(
            rest_module, wrapper_case.rest_function_name
        )
        if metadata is None:
            continue
        cases.append(
            EndpointCase(
                wrapper=wrapper_case,
                operation_name=metadata.operation_name,
                method=metadata.method.lower(),
                path=metadata.path,
            )
        )
    return cases


def service_attr(case: EndpointCase) -> str:
    return case.wrapper.module_path.split(".")[2]
