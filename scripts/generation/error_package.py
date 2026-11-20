# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Service-local error class generation and runtime error-dispatch injection."""

import builtins
import json
import re
from pathlib import Path
from typing import TypedDict

from ._shared import (
    discover_service_model_classes,
    parse_generated_rest_module,
    service_to_pascal_case,
    write_text_lf,
)
from .public_names import operation_key


def error_class_base(method: str, title: str) -> str:
    """The PascalCase stem of a client method's error classes: `list_labels` is `ListLabels`.

    A stem that would make a builtin exception name (`import_` and ImportError)
    gets the Service title in front.
    """
    base = "".join(
        part[:1].upper() + part[1:] for part in method.rstrip("_").split("_")
    )
    return title + base if hasattr(builtins, f"{base}Error") else base


def service_error_class_name(operation_id: str) -> str:
    """Builds a service-local exception name for an OpenAPI operation."""
    return f"{operation_id}Error"


def service_error_response_class_name(operation_id: str, status_code: str) -> str:
    """Builds a leaf error class name for a specific swagger response code."""
    status_name_map = {
        "default": "Unexpected",
        "400": "BadRequest",
        "401": "Unauthorized",
        "402": "PaymentRequired",
        "403": "Forbidden",
        "404": "NotFound",
        "405": "MethodNotAllowed",
        "409": "Conflict",
        "410": "Gone",
        "415": "UnsupportedMediaType",
        "422": "UnprocessableEntity",
        "429": "TooManyRequests",
        "500": "InternalServerError",
        "501": "NotImplemented",
        "502": "BadGateway",
        "503": "ServiceUnavailable",
        "504": "GatewayTimeout",
    }
    suffix = status_name_map.get(status_code, f"Http{status_code}")
    return f"{operation_id}{suffix}Error"


class ErrorResponseMetadata(TypedDict):
    description: str | None
    schema_ref: str | None


class OperationErrorMetadata(TypedDict):
    path: str
    method: str
    responses: dict[str, ErrorResponseMetadata]


def collect_operation_error_responses(
    swagger_path: Path,
) -> dict[str, OperationErrorMetadata]:
    """Extracts non-2xx response metadata for each operation, keyed by operation_key()."""
    with open(swagger_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    operation_errors: dict[str, OperationErrorMetadata] = {}

    for path, methods in schema.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue

        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue

            responses_obj = operation.get("responses", {})
            error_responses: dict[str, ErrorResponseMetadata] = {}

            if isinstance(responses_obj, dict):
                responses: dict[str, object] = responses_obj
                for status_code, response in responses.items():
                    status_code_text = str(status_code)
                    if status_code_text.startswith("2"):
                        continue

                    schema_ref: str | None = None
                    description: str | None = None
                    if isinstance(response, dict):
                        description_raw = response.get("description")
                        if isinstance(description_raw, str):
                            description = description_raw
                        content = response.get("content", {})
                        if isinstance(content, dict):
                            json_content = content.get("application/json", {})
                            if isinstance(json_content, dict):
                                field_schema = json_content.get("schema", {})
                                if isinstance(field_schema, dict):
                                    schema_ref_raw = field_schema.get("$ref")
                                    if isinstance(schema_ref_raw, str):
                                        schema_ref = schema_ref_raw

                    error_responses[status_code_text] = {
                        "description": description,
                        "schema_ref": schema_ref,
                    }

            operation_errors[operation_key(str(method), path)] = {
                "path": path,
                "method": str(method).upper(),
                "responses": error_responses,
            }

    return operation_errors


def merge_operation_error_responses(
    operation_error_sets: list[dict[str, OperationErrorMetadata]],
) -> dict[str, OperationErrorMetadata]:
    """Merges operation error maps from multiple swagger files for one service."""
    merged: dict[str, OperationErrorMetadata] = {}

    for operation_errors in operation_error_sets:
        for operation_id, metadata in operation_errors.items():
            existing = merged.get(operation_id)
            if existing is None:
                merged[operation_id] = {
                    "path": metadata["path"],
                    "method": metadata["method"],
                    "responses": dict(metadata["responses"]),
                }
                continue

            existing["responses"].update(metadata["responses"])

    return merged


def _base_error_class_lines(
    service: str, title: str, status_model: str | None
) -> list[str]:
    """The module header and the Service's base error class.

    status_model is the rpcStatus model's name when the Service defines one.
    """
    imports = [
        "from __future__ import annotations",
        "",
        "from typing import Any",
        "",
        "from kentik_api.errors import HTTPException",
    ]
    if status_model:
        imports += ["", f"from ..models import {status_model}"]

    if status_model:
        message_lines = [
            "            try:",
            f"                status = {status_model}.model_validate(payload)",
            "            except Exception:",
            "                status = None",
            "            if status is not None:",
            # The JSON itself, as gRPC reports it: the model keeps only each detail's @type.
            '                details["rpc_status"] = payload',
            "                if status.code is not None:",
            '                    details["rpc_status_code"] = status.code',
            "                if status.message:",
            "                    message = status.message",
            "                else:",
            '                    message = payload.get("message") or message',
            "            else:",
            '                message = payload.get("message") or message',
        ]
    else:
        message_lines = ['            message = payload.get("message") or message']

    return [
        *imports,
        "",
        f"class {title}Error(HTTPException):",
        f'    """Base service-local error for the {service} API."""',
        "",
        "    @classmethod",
        f'    def _build_error(cls, response: Any, *, operation_name: str, method: str, path: str) -> "{title}Error":',
        '        preview = getattr(response, "text", "")[:200].replace("\\n", " ")',
        '        headers = getattr(response, "headers", {})',
        '        content_type = headers.get("content-type", "unknown") if hasattr(headers, "get") else "unknown"',
        "        details: dict[str, Any] = {",
        '            "content_type": content_type,',
        '            "preview": preview,',
        "        }",
        "        message = f\"{operation_name} failed with status code: {getattr(response, 'status_code', 'unknown')}\"",
        "        try:",
        "            payload = response.json()",
        "        except Exception:",
        "            payload = None",
        "        if isinstance(payload, dict):",
        '            details["response_json"] = payload',
        '            if isinstance(payload.get("error"), str) and payload["error"]:',
        "                message = f\"{message}: {payload['error']}\"",
        *message_lines,
        "        elif payload is not None:",
        '            details["response_json"] = payload',
        "        return cls(",
        '            getattr(response, "status_code", 500),',
        "            message,",
        "            method=method,",
        "            path=path,",
        "            details=details,",
        "        )",
        "",
        "    @classmethod",
        f'    def from_response(cls, response: Any, *, operation_name: str, method: str, path: str) -> "{title}Error":',
        '        status_key = str(getattr(response, "status_code", ""))',
        '        response_error_map = getattr(cls, "response_error_map", {})',
        '        target_cls = response_error_map.get(status_key) or response_error_map.get("default") or cls',
        "        return target_cls._build_error(",
        "            response,",
        "            operation_name=operation_name,",
        "            method=method,",
        "            path=path,",
        "        )",
        "",
    ]


def _operation_error_class_lines(
    service: str,
    title: str,
    method: str,
    base: str,
    metadata: OperationErrorMetadata,
) -> tuple[str, list[str], list[str]]:
    """One operation's error class, its per-status classes, and their source lines."""
    operation_class = service_error_class_name(base)
    leaf_classes: list[str] = []
    mapping_entries: list[str] = []
    # The operation class comes first so each response class can extend it,
    # which makes `except <Operation>Error` catch every error the call raises.
    lines = [
        "",
        f"class {operation_class}({title}Error):",
        f'    """Operation-local error for client.{service}.{method}()."""',
        f"    response_error_map: dict[str, type[{title}Error]] = {{}}",
    ]
    for status_code, response in sorted(
        metadata["responses"].items(), key=lambda item: item[0]
    ):
        description = " ".join((response["description"] or "").split())
        schema_ref = response["schema_ref"] or ""
        leaf_class = service_error_response_class_name(base, status_code)
        leaf_classes.append(leaf_class)
        response_bits = f"{status_code}: {description} {schema_ref}".strip()
        leaf_doc = (
            f"Operation-local response error for {method} ({response_bits})."
            if response_bits
            else f"Operation-local response error for {method}."
        )
        # Schema text: escaped like the templates' docstring macro.
        leaf_doc = leaf_doc.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
        lines += [
            "",
            f"class {leaf_class}({operation_class}):",
            f'    """{leaf_doc}"""',
            "    pass",
        ]
        mapping_entries.append(f'    "{status_code}": {leaf_class},')

    lines += [
        "",
        f"{operation_class}.response_error_map = {{",
        *mapping_entries,
        "}",
    ]
    return operation_class, leaf_classes, lines


def generate_service_error_package(
    service_dir: Path,
    operation_errors: dict[str, OperationErrorMetadata],
    method_names: dict[tuple[Path, str], str],
    status_model: str | None = "rpcStatus",
) -> None:
    """Writes a Service's error package and points each REST function at its error class.

    method_names maps each (REST module, function) to its client method, which
    names the operation's error classes. status_model is the public name of the
    schema's `rpcStatus` model.
    """
    service = service_dir.name
    title = service_to_pascal_case(service)
    model_classes = discover_service_model_classes(service_dir)
    functions = {
        rest_file: {op.name: op for op in parse_generated_rest_module(rest_file)}
        for rest_file, _ in method_names
    }
    method_by_key = {
        operation_key(op.http_method, op.path): method
        for (rest_file, name), method in method_names.items()
        for op in [functions[rest_file][name]]
    }
    if set(method_by_key) != set(operation_errors):
        raise ValueError(
            f"{service}: the swagger and REST operations differ: "
            f"{sorted(set(method_by_key) ^ set(operation_errors))}"
        )
    base_by_method = {
        method: error_class_base(method, title) for method in method_by_key.values()
    }

    error_dir = service_dir / "error"
    error_dir.mkdir(exist_ok=True)

    lines = _base_error_class_lines(
        service, title, status_model if status_model in model_classes else None
    )

    leaf_class_names: list[str] = []
    operation_class_names: list[str] = []
    for key, method in sorted(method_by_key.items(), key=lambda item: item[1]):
        operation_class, leaf_classes, class_lines = _operation_error_class_lines(
            service, title, method, base_by_method[method], operation_errors[key]
        )
        operation_class_names.append(operation_class)
        leaf_class_names.extend(leaf_classes)
        lines.extend(class_lines)

    lines.extend(
        [
            "",
            f"ERROR_BY_METHOD: dict[str, type[{title}Error]] = {{",
        ]
    )

    for method in sorted(base_by_method):
        lines.append(
            f'    "{method}": {service_error_class_name(base_by_method[method])},'
        )

    lines.extend(
        [
            "}",
            "",
            f'__all__ = ["{title}Error",',
        ]
    )
    for leaf_class in leaf_class_names:
        lines.append(f'    "{leaf_class}",')
    for operation_class in operation_class_names:
        lines.append(f'    "{operation_class}",')
    lines.extend(
        [
            '    "ERROR_BY_METHOD",',
            "]",
            "",
        ]
    )

    class_names = [f"{title}Error", *operation_class_names, *leaf_class_names]
    repeated = sorted({n for n in class_names if class_names.count(n) > 1})
    if repeated:
        raise ValueError(f"{service}: error class names are not unique: {repeated}")

    write_text_lf(error_dir / "__init__.py", "\n".join(lines))

    for rest_file in functions:
        error_classes = {
            name: service_error_class_name(base_by_method[method])
            for (path, name), method in method_names.items()
            if path == rest_file
        }
        content = rest_file.read_text(encoding="utf-8")
        write_text_lf(rest_file, inject_service_error_handling(content, error_classes))


def inject_service_error_handling(content: str, error_classes: dict[str, str]) -> str:
    """Points each REST function at its error class and imports those classes.

    error_classes maps function name to error class. Replaces the
    # __ERROR_IMPORTS_PLACEHOLDER__ sentinel that service.jinja2 emits, or
    falls back to the request_json import anchor.
    """
    _PLACEHOLDER = "# __ERROR_IMPORTS_PLACEHOLDER__"

    parts = re.split(r"(?m)^(?=def \w+\()", content)
    for i, part in enumerate(parts):
        function = re.match(r"def (\w+)\(", part)
        if function and function.group(1) in error_classes:
            parts[i] = re.sub(
                r"error_cls=\w+", f"error_cls={error_classes[function.group(1)]}", part
            )
    content = "".join(parts)

    if not error_classes:
        return content.replace("\n" + _PLACEHOLDER, "")

    import_line = "from ..error import " + ", ".join(
        sorted(set(error_classes.values()))
    )

    if _PLACEHOLDER in content:
        return content.replace(_PLACEHOLDER, import_line)

    runtime_import = "from kentik_api.core.rest_runtime import request_json\n"
    if runtime_import in content:
        return content.replace(
            runtime_import,
            runtime_import + "\n" + import_line + "\n",
            1,
        )

    raise ValueError(
        "inject_service_error_handling: expected either '# __ERROR_IMPORTS_PLACEHOLDER__' "
        "or 'from kentik_api.core.rest_runtime import request_json' anchor. "
        "If rest_runtime was moved or renamed, update this function."
    )
