# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Per-endpoint documentation: extracted from swagger while the schema is available,
rendered as Sphinx MyST stubs later, once wrapper method signatures exist.

EndpointDocsCollector accumulates the extract() results across the
schema-availability loop. It does not enforce the two-phase ordering:
render() reads wrapper signatures off disk, so it must run after service
wrapper generation, and that remains the caller's responsibility.
"""

import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import FunctionType

from . import diagram_kit as dk
from ._shared import (
    PROJECT_ROOT,
    REGENERATE_COMMAND,
    GrpcCall,
    discover_service_model_classes,
    grpc_call,
    grpc_stub_services,
    iter_service_dirs,
    mermaid_init,
    parse_wrapper_methods,
    service_to_pascal_case,
    write_text_lf,
)
from .explorer_docs import fragment

MD_FENCE = "`" * 3
SCHEMA_RECORD_FILE = PROJECT_ROOT / "schema_operations.json"
_MD_HEADING = re.compile(r"^(#{1,6})(?=\s)")


def _provenance(writer: FunctionType) -> str:
    """Builds the AUTO-GENERATED header naming the code that wrote the file.

    Derived from the writer rather than typed out, so renaming it cannot leave
    the header pointing at a function that no longer exists.
    """
    module_path = Path(sys.modules[writer.__module__].__file__ or "").resolve()
    try:
        rel = module_path.relative_to(PROJECT_ROOT)
    except ValueError:
        rel = Path(module_path.name)
    return f"<!-- AUTO-GENERATED: {rel.as_posix()}, {writer.__name__}() -->"


@dataclass(frozen=True)
class EndpointParam:
    name: str
    location: str
    type_label: str
    required: bool


@dataclass(frozen=True)
class EndpointResponse:
    status: str
    description: str
    type_label: str


@dataclass(frozen=True)
class EndpointDoc:
    tag: str
    method: str
    path: str
    operation_id: str
    summary: str
    description: str
    parameters: list[EndpointParam]
    request_body: EndpointParam | None
    responses: list[EndpointResponse]


def _schema_type_label(schema: object) -> str:
    """Renders a short, human-readable type label for an OpenAPI schema object."""
    if not isinstance(schema, dict):
        return "-"
    ref = schema.get("$ref")
    if isinstance(ref, str) and ref:
        return ref.rsplit("/", 1)[-1]
    if schema.get("type") == "array":
        return f"{_schema_type_label(schema.get('items'))}[]"
    schema_type = schema.get("type")
    if isinstance(schema_type, str) and schema_type:
        fmt = schema.get("format")
        return f"{schema_type} ({fmt})" if isinstance(fmt, str) and fmt else schema_type
    return "object"


_METHOD_ORDER = ("get", "post", "put", "patch", "delete", "options", "head", "trace")


def extract_endpoint_docs(swagger_path: Path) -> list[EndpointDoc]:
    """Extracts per-operation documentation (params, every response) from a swagger file.

    Unlike collect_operation_error_responses (which only looks at non-2xx
    responses, for error-class generation), this captures every declared
    response so it can be rendered as real Sphinx text (tables and a
    generated usage example) instead of a rendered diagram image.
    """
    with open(swagger_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    tags_raw = schema.get("tags") if isinstance(schema.get("tags"), list) else []
    default_tag = next(
        (
            str(tag["name"]).strip()
            for tag in tags_raw
            if isinstance(tag, dict) and tag.get("name")
        ),
        None,
    )
    paths_obj = schema.get("paths") if isinstance(schema.get("paths"), dict) else {}

    docs: list[EndpointDoc] = []
    for endpoint, methods in sorted(paths_obj.items(), key=lambda item: item[0]):
        if not isinstance(methods, dict):
            continue
        for method in _METHOD_ORDER:
            op = methods.get(method)
            if isinstance(op, dict):
                docs.append(_endpoint_doc(str(endpoint), method, op, default_tag))
    return docs


def _endpoint_doc(
    endpoint: str, method: str, op: dict, default_tag: str | None
) -> EndpointDoc:
    """One operation's documentation: its tag, parameters, body, and every response."""
    op_tags = op.get("tags")
    body = op.get("requestBody")
    responses = op.get("responses")
    return EndpointDoc(
        tag=next(
            (
                str(item).strip()
                for item in (op_tags if isinstance(op_tags, list) else [])
                if isinstance(item, str) and str(item).strip()
            ),
            default_tag or "default",
        ),
        method=method.upper(),
        path=endpoint,
        operation_id=str(op.get("operationId") or "-"),
        summary=str(op.get("summary") or ""),
        description=str(op.get("description") or ""),
        parameters=[
            EndpointParam(
                name=str(param.get("name") or "-"),
                location=str(param.get("in") or "-"),
                type_label=_schema_type_label(param.get("schema")),
                required=bool(param.get("required", False)),
            )
            for param in op.get("parameters") or []
            if isinstance(param, dict)
        ],
        request_body=(
            EndpointParam(
                name="data",
                location="body",
                type_label=_json_type_label(body),
                required=bool(body.get("required", False)),
            )
            if isinstance(body, dict)
            else None
        ),
        responses=[
            EndpointResponse(
                status=str(status),
                description=str(resp.get("description") or "-"),
                type_label=_json_type_label(resp),
            )
            for status, resp in (
                sorted(responses.items()) if isinstance(responses, dict) else []
            )
            if isinstance(resp, dict)
        ],
    )


def _json_type_label(body_or_response: dict) -> str:
    """The type label of a request body's or a response's application/json schema."""
    content = body_or_response.get("content", {})
    json_content = (
        content.get("application/json", {}) if isinstance(content, dict) else {}
    )
    return _schema_type_label(
        json_content.get("schema") if isinstance(json_content, dict) else None
    )


def _md_cell(value: str) -> str:
    """Escapes text for safe use inside a single Markdown table cell."""
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text.replace("|", "\\|") or "-"


def _normalize_path_for_matching(path: str) -> str:
    """Strips dots from path-parameter placeholders (`{device.id}` -> `{deviceid}`)
    so a raw-schema path and its generated-code path template compare equal.
    """
    return re.sub(r"\{([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\}", r"{\1\2}", path)


def _rest_function_path_and_method(
    rest_file: Path, function_name: str
) -> tuple[str, str] | None:
    """Returns (HTTP_METHOD_UPPER, path) for a named function in a generated REST module."""
    from ._shared import parse_generated_rest_module

    for op in parse_generated_rest_module(rest_file):
        if op.name == function_name:
            return op.http_method.upper(), op.path
    return None


WrapperSignatures = dict[
    tuple[str, str], tuple[str, list[tuple[str, str, bool]], GrpcCall | None]
]


def parse_wrapper_method_signatures(wrapper_file: Path) -> WrapperSignatures:
    """Maps (http_method, normalized_path) -> (wrapper_method_name, params, grpc_call).

    grpc_call is None when the method raises NotImplementedError on gRPC.

    Keyed by method+path rather than operationId: multi-swagger-file
    services legitimately reuse generic operationIds like "List"/"Get"
    across different underlying REST modules (e.g. alerting's AlertService
    and SuppressionService both declare an operationId of exactly "List"),
    so operationId alone can't disambiguate which wrapper method an
    EndpointDoc (extracted straight from one swagger file) corresponds to.
    Method+path is guaranteed unique: OpenAPI forbids two operations
    sharing both within one merged service.

    Reads the actual generated ServiceWrapper class and its underlying REST
    module (via AST, no import/execution) so example snippets always match
    the real, callable signature, including flattened nested-object
    parameter names like `pagination.limit` -> `paginationlimit` that only
    exist post-generation.
    """
    method_params = {
        m.name: list(m.params) for m in parse_wrapper_methods(wrapper_file)
    }
    if not method_params:
        return {}

    try:
        tree = ast.parse(
            wrapper_file.read_text(encoding="utf-8"), filename=str(wrapper_file)
        )
    except OSError:
        return {}

    module_alias_to_file = _rest_module_files(tree, wrapper_file.parent)
    wrapper_class = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name.endswith("ServiceWrapper")
        ),
        None,
    )
    if wrapper_class is None:
        return {}

    init = next(
        (
            n
            for n in wrapper_class.body
            if isinstance(n, ast.FunctionDef) and n.name == "__init__"
        ),
        None,
    )
    stub_services = grpc_stub_services(init) if init else {}

    mapping: WrapperSignatures = {}
    for node in wrapper_class.body:
        if not isinstance(node, ast.FunctionDef) or node.name == "__init__":
            continue

        params = method_params.get(node.name)
        if params is None:
            continue

        rest_call = _rest_call(node)
        if rest_call is None:
            continue
        rest_alias, operation_id = rest_call

        rest_file = module_alias_to_file.get(rest_alias)
        if rest_file is None:
            continue
        metadata = _rest_function_path_and_method(rest_file, operation_id)
        if metadata is None:
            continue
        http_method, path_template = metadata

        mapping[(http_method, _normalize_path_for_matching(path_template))] = (
            node.name,
            params,
            grpc_call(node, stub_services),
        )

    return mapping


def _rest_module_files(tree: ast.Module, services_folder: Path) -> dict[str, Path]:
    """Maps each REST module alias a wrapper imports to that module's file."""
    files: dict[str, Path] = {}
    for node in tree.body:
        if not isinstance(node, ast.Import):
            continue
        for alias in node.names:
            if not alias.asname or "." not in alias.name:
                continue
            candidate = services_folder / f"{alias.name.rsplit('.', 1)[-1]}.py"
            if candidate.exists():
                files[alias.asname] = candidate
    return files


def _rest_call(method: ast.FunctionDef) -> tuple[str, str] | None:
    """(REST module alias, function name) of the REST call a wrapper method returns."""
    for sub in ast.walk(method):
        if (
            isinstance(sub, ast.Return)
            and isinstance(sub.value, ast.Call)
            and isinstance(sub.value.func, ast.Attribute)
            and isinstance(sub.value.func.value, ast.Name)
            and sub.value.func.value.id.startswith("Rest")
        ):
            return sub.value.func.value.id, sub.value.func.attr
    return None


def _example_value_for_annotation(
    annotation_text: str, name: str, models: set[str] | None = None
) -> str:
    """Builds a plausible Python source snippet for a parameter's example value.

    Adds each model class the snippet constructs to models, so the caller can
    import it.
    """
    text = annotation_text.strip()
    if text.startswith("Optional[") and text.endswith("]"):
        text = text[len("Optional[") : -1].strip()
    for list_prefix in ("List[", "list["):
        if text.startswith(list_prefix) and text.endswith("]"):
            inner = text[len(list_prefix) : -1].strip()
            return f"[{_example_value_for_annotation(inner, name, models)}]"

    if text == "str":
        return f'"{name}-example"'
    if text == "int":
        return "1"
    if text == "float":
        return "1.0"
    if text == "bool":
        return "True"
    if text == "bytes":
        return 'b"example"'
    if text in ("Any", ""):
        return "..."
    if text.startswith(("Dict[", "dict[")):
        return "{}"

    class_name = text.rsplit(".", 1)[-1]
    if models is not None:
        models.add(class_name)
    return f"{class_name}(...)"


def _render_example_snippet(
    service: str,
    method_name: str,
    params: list[tuple[str, str, bool]],
    rest_only: bool = False,
) -> str:
    """Renders a runnable-looking usage example from a real wrapper method signature."""
    models: set[str] = set()
    arguments = [
        f"    {param_name}={_example_value_for_annotation(annotation_text, param_name, models)},"
        for param_name, annotation_text, required in params
        if required
    ]
    lines = ["from kentik_api.client import KentikAPI"]
    if models:
        lines.append(
            f"from kentik_api.gen.{service}.models import {', '.join(sorted(models))}"
        )
    lines += [
        "",
        '# REST only. A client created with protocol="grpc" also sends these calls over REST.'
        if rest_only
        else '# Both transports work: protocol="rest" (default) or protocol="grpc".',
        'client = KentikAPI(protocol="rest")  # loads KENTIK_EMAIL/KENTIK_API_TOKEN from .env',
    ]
    if arguments:
        lines += [f"response = client.{service}.{method_name}(", *arguments, ")"]
    else:
        lines.append(f"response = client.{service}.{method_name}()")
    return "\n".join(lines)


def _render_operation_sequence_diagram(
    service: str,
    doc: EndpointDoc,
    method_name: str,
    params: list[tuple[str, str, bool]],
    grpc_call: GrpcCall | None,
    sub_heading: str,
    rest_only: bool = False,
) -> list[str]:
    """Renders REST and gRPC sequence diagrams side by side for one operation."""
    req_params = [(p, t) for p, t, r in params if r]
    if req_params:
        call_args = ", ".join(
            f"{p}={_example_value_for_annotation(t, p)}" for p, t in req_params
        )
    else:
        call_args = ""

    success_resp = next((r for r in doc.responses if r.status.startswith("2")), None)
    success_model = success_resp.type_label if success_resp else "response"

    rest_diagram = [
        f"{sub_heading} REST call flow",
        "",
        f"{MD_FENCE}mermaid",
        mermaid_init(),
        "sequenceDiagram",
        "    actor C as Caller",
        f'    participant W@{{ "type": "boundary" }} as client.{service}',
        "    participant API as Kentik REST API",
        "",
        f"    C->>+W: {method_name}({call_args})",
        f"    W->>+API: {doc.method} {doc.path}",
        "    alt success",
        f"        API-->>W: {success_model} (JSON)",
        f"        W-->>C: {success_model}",
        "    else error status",
        "        API-->>W: error body",
        "        W-->>C: raise AuthenticationError (401) or HTTPException",
        "    else no response",
        "        W-->>C: raise TransportError",
        "    end",
        "    deactivate API",
        "    deactivate W",
        MD_FENCE,
        "",
    ]

    if rest_only:
        grpc_diagram = [
            f"{sub_heading} gRPC call flow",
            "",
            (
                "Not used. This endpoint exists only on REST. A client with "
                '`protocol="grpc"` also sends this call over REST.'
            ),
            "",
        ]
        return rest_diagram + grpc_diagram

    if grpc_call is None:
        grpc_diagram = [
            f"{sub_heading} gRPC call flow",
            "",
            (
                "Not available. No RPC declares the HTTP rule of this operation. On "
                '`protocol="grpc"`, this method raises `NotImplementedError`. Call it '
                'through a `protocol="rest"` client.'
            ),
            "",
        ]
        return rest_diagram + grpc_diagram

    grpc_diagram = [
        f"{sub_heading} gRPC call flow",
        "",
        f"{MD_FENCE}mermaid",
        mermaid_init(),
        "sequenceDiagram",
        "    actor C as Caller",
        f'    participant W@{{ "type": "boundary" }} as client.{service}',
        '    participant R@{ "type": "control" } as grpc_runtime',
        "    participant API as Kentik gRPC API",
        "",
        f"    C->>+W: {method_name}({call_args})",
        f"    W->>+R: build_grpc_request({grpc_call.request}, arguments)",
        f"    R->>+API: {grpc_call.rpc} (gRPC/TLS)",
        "    alt success",
        "        API-->>R: response message",
        "        R-->>W: parse_grpc_response(response)",
        f"        W-->>C: {success_model}",
        "    else gRPC error, deadline, or unreachable",
        "        R-->>W: map_grpc_error()",
        "        W-->>C: raise AuthenticationError, HTTPException, or TransportError",
        "    end",
        "    deactivate API",
        "    deactivate R",
        "    deactivate W",
        MD_FENCE,
        "",
    ]

    return rest_diagram + grpc_diagram


def _nest_headings(text: str, top_level: int) -> str:
    """Shifts schema-prose headings so the highest sits at `top_level`.

    A description's own `###` would otherwise break the page outline.
    """
    lines = text.split("\n")
    in_fence = False
    headings: dict[int, int] = {}
    for row, line in enumerate(lines):
        if line.lstrip().startswith(MD_FENCE):
            in_fence = not in_fence
        elif not in_fence and (match := _MD_HEADING.match(line)):
            headings[row] = len(match.group(1))
    if not headings:
        return text
    shift = top_level - min(headings.values())
    for row, level in headings.items():
        lines[row] = "#" * min(level + shift, 6) + lines[row][level:]
    return "\n".join(lines)


def _render_endpoint_section(
    service: str,
    doc: EndpointDoc,
    wrapper_signatures: WrapperSignatures,
    heading_level: int = 4,
    rest_only: bool = False,
) -> list[str]:
    heading = "#" * heading_level
    sub_heading = "#" * (heading_level + 1)

    signature = wrapper_signatures.get(
        (doc.method, _normalize_path_for_matching(doc.path))
    )
    method_name, params, grpc_call = signature if signature else (None, [], None)

    lines = [f"{heading} `{doc.method}` `{doc.path}`", ""]
    if doc.summary:
        lines.extend([doc.summary, ""])
    if doc.description and doc.description != doc.summary:
        lines.extend([_nest_headings(doc.description, heading_level + 1), ""])

    if method_name is not None:
        lines.extend(
            _render_operation_sequence_diagram(
                service, doc, method_name, params, grpc_call, sub_heading, rest_only
            )
        )

    all_params = list(doc.parameters)
    if doc.request_body:
        all_params.append(doc.request_body)

    if all_params:
        lines.extend(
            [
                f"{sub_heading} Parameters",
                "",
                "| Name | In | Type | Required |",
                "| --- | --- | --- | --- |",
            ]
        )
        for param in all_params:
            # Generated wrapper methods flatten dotted nested-object params
            # (e.g. schema `asGroup.id` -> kwarg `asGroupid`); show the name
            # callers actually type, matching the example below.
            display_name = param.name.replace(".", "")
            lines.append(
                f"| `{_md_cell(display_name)}` | {_md_cell(param.location)} | "
                f"`{_md_cell(param.type_label)}` | {'Yes' if param.required else 'No'} |"
            )
        lines.append("")

    if doc.responses:
        lines.extend(
            [
                f"{sub_heading} Responses",
                "",
                "| Status | Description | Model |",
                "| --- | --- | --- |",
            ]
        )
        for resp in doc.responses:
            lines.append(
                f"| {_md_cell(resp.status)} | {_md_cell(resp.description)} | "
                f"`{_md_cell(resp.type_label)}` |"
            )
        lines.append("")

    if method_name is not None:
        lines.extend(
            [
                f"{sub_heading} Example",
                "",
                f"{MD_FENCE}python",
                _render_example_snippet(service, method_name, params, rest_only),
                MD_FENCE,
                "",
            ]
        )

    return lines


def _autodoc_directive_for_model(models_dir: Path, class_name: str) -> str:
    """Picks the right autodoc directive for a generated model class.

    Most generated classes are Pydantic BaseModel subclasses, which
    sphinxcontrib.autodoc_pydantic renders beautifully via
    `autopydantic_model`. But OpenAPI enum schemas generate plain
    `class X(str, Enum)` classes. Feeding those into autopydantic_model
    crashes the Sphinx build (it assumes `__pydantic_decorators__` exists),
    so they need the standard `autoclass` directive instead.
    """
    model_file = models_dir / f"{class_name}.py"
    try:
        tree = ast.parse(
            model_file.read_text(encoding="utf-8"), filename=str(model_file)
        )
    except OSError:
        return "autopydantic_model"

    for node in tree.body:
        if not (isinstance(node, ast.ClassDef) and node.name == class_name):
            continue
        for base in node.bases:
            base_name = ast.unparse(base)
            if base_name.rsplit(".", 1)[-1] == "BaseModel":
                return "autopydantic_model"
        return "autoclass"

    return "autopydantic_model"


def _model_reference_edges(
    models_dir: Path, model_classes: list[str]
) -> dict[str, dict[str, list[str]]]:
    """Maps each model to the sibling models its fields name, with those field names.

    Parses annotations statically (no import) and matches sibling class names
    by word boundary, so `items: Optional[List[FooConfig]]` yields an edge to
    `FooConfig` labeled `items` when `FooConfig` is another model in the same service.
    """
    names = set(model_classes)
    edges: dict[str, dict[str, list[str]]] = {}
    for cls in model_classes:
        refs: dict[str, list[str]] = {}
        model_file = models_dir / f"{cls}.py"
        try:
            tree = ast.parse(
                model_file.read_text(encoding="utf-8"), filename=str(model_file)
            )
        except OSError:
            edges[cls] = refs
            continue
        for node in ast.walk(tree):
            if not (
                isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name)
            ):
                continue
            text = ast.unparse(node.annotation)
            for other in names:
                if other != cls and re.search(rf"\b{re.escape(other)}\b", text):
                    refs.setdefault(other, []).append(node.target.id)
        edges[cls] = refs
    return edges


# Cap the model class diagram so dense services (e.g. alerting's 185 models)
# stay legible and don't overwhelm the browser-side Mermaid renderer.
_MODEL_DIAGRAM_MAX_NODES = 30


def _render_model_relationship_diagram(
    endpoint_docs: list[EndpointDoc],
    models_dir: Path,
    model_classes: list[str],
) -> list[str]:
    """Renders a collapsible Mermaid classDiagram of the service's model graph.

    Focuses on the public surface (the request/response models the operations
    use, plus the models they directly reference) and falls back to the
    service's own models for schema-only services. Caps the node count so dense
    services stay readable.
    """
    if not model_classes:
        return []

    edges = _model_reference_edges(models_dir, model_classes)
    names = set(model_classes)

    entry: set[str] = set()
    for doc in endpoint_docs:
        labels = [r.type_label for r in doc.responses]
        if doc.request_body:
            labels.append(doc.request_body.type_label)
        for label in labels:
            base = label.replace("[]", "").strip()
            if base in names:
                entry.add(base)

    if not entry:
        entry = set(model_classes)

    nodes: set[str] = set(entry)
    for cls in entry:
        nodes |= set(edges.get(cls, {}))

    if len(nodes) > _MODEL_DIAGRAM_MAX_NODES:
        nodes = set(sorted(nodes)[:_MODEL_DIAGRAM_MAX_NODES])

    shown_edges = sorted(
        (src, dst, fields)
        for src in nodes
        for dst, fields in edges.get(src, {}).items()
        if dst in nodes
    )

    diagram = [mermaid_init(), "classDiagram"]
    for name in sorted(nodes):
        diagram.append(f"    class {name}")
    for src, dst, fields in shown_edges:
        label = ", ".join(fields[:2]) + (", ..." if len(fields) > 2 else "")
        diagram.append(f"    {src} --> {dst} : {label}")

    summary = f"Model relationships ({len(nodes)} of {len(model_classes)} models)"
    return [
        "<details>",
        f"<summary>{summary}</summary>",
        "",
        "Each arrow points from a model to a model that one of its fields holds. The label names the field.",
        "",
        f"{MD_FENCE}mermaid",
        *diagram,
        MD_FENCE,
        "",
        "</details>",
        "",
    ]


_OV_COLS = (160, 450, 740)
_OV_ROWS = (30, 170, 310, 450, 590)


def _render_service_overview(
    service: str,
    group_order: list[str],
    grouped: dict[str, list[EndpointDoc]],
    rest_only: bool,
) -> list[str]:
    """Renders the call path of this service as an explorer, from your code down to the Kentik API.

    Each hop is a call (down) and its answer (up), so selecting a part shows what
    answers it and what waits for it. Returns nothing for schema-only services.
    """
    if not group_order:
        return []

    title = service_to_pascal_case(service)
    operations = sum(len(docs) for docs in grouped.values())
    p = "ov"
    # part: (column, row, family, kind, box lines, card title, role, facts, if it stops)
    parts: dict[str, tuple[int, int, str, str, list[str], str, str, list[str], str]] = {
        "code": (
            1,
            0,
            "green",
            "src",
            ["Your code", f"client.{service}"],
            "Your code",
            "Calls a method on the service wrapper.",
            [f"client.{service}.<method>(...)"],
            "Nothing in the SDK runs.",
        ),
        "wrap": (
            1,
            1,
            "orange",
            "proc",
            [f"{title}ServiceWrapper", f"client.{service}", f"{operations} operations"],
            f"{title}ServiceWrapper",
            "Sends each call to the REST function or to call_grpc(), for the transport that the client uses.",
            [
                f"Source: gen/{service}/services/{service}.py",
                f"Returns models from gen/{service}/models/",
            ],
            "Expected: no operation of this service can be called.",
        ),
        "rest": (
            0,
            2,
            "blue",
            "proc",
            ["REST functions", f"gen/{service}/services/"],
            "REST functions",
            "One function per operation. Each one calls request_json() with its own error class.",
            [f"Error classes: gen/{service}/error/"],
            "Expected: calls on a REST transport fail. A gRPC client keeps working.",
        ),
        "rj": (
            0,
            3,
            "blue",
            "proc",
            ["request_json()", "core/rest_runtime.py"],
            "request_json()",
            "The one function that sends REST traffic: auth headers, quota, and errors.",
            [
                "Raises AuthenticationError on 401",
                "Raises the operation's error class on other errors",
            ],
            "Expected: every REST call of every service fails.",
        ),
        "restapi": (
            0,
            4,
            "blue",
            "src",
            ["Kentik REST API", "HTTPS + JSON"],
            "Kentik REST API",
            "The REST endpoints of the service.",
            ["Reports the quota in response headers"],
            "Expected: REST calls raise TransportError. A gRPC client keeps working.",
        ),
    }
    # wire id: (path, links, label, label position, anchor, kind)
    wires: list[tuple[str, str, str, str, tuple[int, int], str, str]] = [
        (
            "code_call",
            "M520,102 V170",
            "code>wrap",
            "method call",
            (512, 140),
            "end",
            "call",
        ),
        (
            "wrap_answer",
            "M580,170 V102",
            "wrap>code",
            "Pydantic model",
            (588, 140),
            "start",
            "data",
        ),
        (
            "rest_call",
            "M450,196 H230 V310",
            "wrap>rest",
            "arguments",
            (340, 188),
            "middle",
            "call",
        ),
        (
            "rest_answer",
            "M290,310 V226 H450",
            "rest>wrap",
            "Pydantic model",
            (298, 275),
            "start",
            "data",
        ),
        (
            "rj_call",
            "M230,382 V450",
            "rest>rj",
            "method, path, body",
            (222, 420),
            "end",
            "call",
        ),
        (
            "rj_answer",
            "M290,450 V382",
            "rj>rest",
            "JSON dict",
            (298, 420),
            "start",
            "data",
        ),
        (
            "api_call",
            "M230,522 V590",
            "rj>restapi",
            "HTTPS request",
            (222, 560),
            "end",
            "call",
        ),
        (
            "api_answer",
            "M290,590 V522",
            "restapi>rj",
            "JSON response",
            (298, 560),
            "start",
            "data",
        ),
    ]
    if rest_only:
        # One path only, so it runs straight down the middle.
        parts = {
            pid: (1, row, fam, kind, lines, name, role, facts, stops)
            for pid, (
                _,
                row,
                fam,
                kind,
                lines,
                name,
                role,
                facts,
                stops,
            ) in parts.items()
        }
        hops = [
            ("wrap", "rest", "arguments", "Pydantic model", 242),
            ("rest", "rj", "method, path, body", "JSON dict", 382),
            ("rj", "restapi", "HTTPS request", "JSON response", 522),
        ]
        wires = wires[:2] + [
            wire
            for upper, lower, ask, answer, y in hops
            for wire in (
                (
                    f"{lower}_call",
                    f"M520,{y} V{y + 68}",
                    f"{upper}>{lower}",
                    ask,
                    (512, y + 38),
                    "end",
                    "call",
                ),
                (
                    f"{lower}_answer",
                    f"M580,{y + 68} V{y}",
                    f"{lower}>{upper}",
                    answer,
                    (588, y + 38),
                    "start",
                    "data",
                ),
            )
        ]
    rest_path = [
        "code>wrap",
        "wrap>rest",
        "rest>rj",
        "rj>restapi",
        "restapi>rj",
        "rj>rest",
        "rest>wrap",
        "wrap>code",
    ]
    paths = {
        "rest": {
            "label": "REST call",
            "family": "blue",
            "title": "A call on a REST transport",
            "text": "The wrapper calls the REST function, which sends the request with request_json().",
            "links": rest_path,
        }
    }
    if not rest_only:
        parts |= {
            "cg": (
                2,
                2,
                "violet",
                "proc",
                ["call_grpc()", "core/grpc_runtime.py"],
                "call_grpc()",
                "The one function that sends gRPC traffic: deadline, quota, and errors.",
                ["Parses each answer into the same models as REST"],
                "Expected: every gRPC call fails. A REST client keeps working.",
            ),
            "grpcapi": (
                2,
                4,
                "violet",
                "src",
                ["Kentik gRPC API", "HTTP/2 + protobuf"],
                "Kentik gRPC API",
                "The gRPC methods of the service.",
                ["Reports the quota in response metadata"],
                "Expected: gRPC calls raise TransportError. A REST client keeps working.",
            ),
        }
        wires += [
            (
                "cg_call",
                "M650,196 H870 V310",
                "wrap>cg",
                "proto request",
                (760, 188),
                "middle",
                "call",
            ),
            (
                "cg_answer",
                "M810,310 V226 H650",
                "cg>wrap",
                "proto response",
                (802, 275),
                "end",
                "data",
            ),
            (
                "grpc_call",
                "M810,382 V590",
                "cg>grpcapi",
                "gRPC call",
                (802, 490),
                "end",
                "call",
            ),
            (
                "grpc_answer",
                "M870,590 V382",
                "grpcapi>cg",
                "proto response",
                (878, 490),
                "start",
                "data",
            ),
        ]
        paths["grpc"] = {
            "label": "gRPC call",
            "family": "violet",
            "title": "A call on a gRPC transport",
            "text": "The wrapper builds the proto request and sends it with call_grpc().",
            "links": [
                "code>wrap",
                "wrap>cg",
                "cg>grpcapi",
                "grpcapi>cg",
                "cg>wrap",
                "wrap>code",
            ],
        }

    segs = [
        dk.seg(sid, d, [key], p, label, at, anchor=anchor, kind=kind)
        for sid, d, key, label, at, anchor, kind in wires
    ]
    boxes = [
        dk.node(
            pid, (_OV_COLS[col], _OV_ROWS[row], 200, 72), fam, kind, lines, label=name
        )
        for pid, (col, row, fam, kind, lines, name, *_) in parts.items()
    ]
    markup = dk.svg(
        "overview-svg",
        (1100, 680),
        f"Call path of client.{service}: your code calls the wrapper, which sends the call over REST"
        + ("." if rest_only else " or gRPC."),
        "".join(segs + boxes),
        p,
    )
    data = {
        "select": "wrap",
        "parts": {
            pid: {"title": name, "role": role, "facts": facts, "stops": stops}
            for pid, (*_, name, role, facts, stops) in parts.items()
        },
        "paths": paths,
    }
    caption = (
        "Select a part. Each hop is a call going down and its answer coming back up."
        + (
            " This service is REST only, so a gRPC client also sends its calls over REST."
            if rest_only
            else ""
        )
    )
    return [
        "## Overview",
        "",
        *fragment(markup, data, caption),
        "",
        (
            f"On an error status or a failed call, the SDK raises an error class from "
            f"`gen/{service}/error/`, or a shared type from `kentik_api.errors`."
        ),
        "",
    ]


def render_endpoint_docs(
    service_endpoint_docs: dict[str, list[EndpointDoc]],
    rest_only: frozenset[str] = frozenset(),
):
    """Generates Sphinx MyST stubs with real per-endpoint text and model docs.

    Replaces an image-rendered "API table" (unreadable once summaries/
    descriptions got long, and rendered even for swagger files with zero
    operations) with real MyST tables plus an auto-generated usage example
    per endpoint, and replaces image-rendered model class diagrams (illegible
    once a service has more than a couple dozen models, e.g. alerting's 185)
    with sphinxcontrib.autodoc_pydantic's per-model field/JSON-schema docs.
    """
    print("Generating Sphinx documentation stubs...")

    DOCS_SERVICES_DIR = PROJECT_ROOT / "docs" / "sphinx" / "services"
    DOCS_SERVICES_DIR.mkdir(parents=True, exist_ok=True)

    for stale in DOCS_SERVICES_DIR.glob("*.md"):
        stale.unlink()

    services = [service_dir.name for service_dir in iter_service_dirs()]
    for service_dir in iter_service_dirs():
        service = service_dir.name
        write_text_lf(
            DOCS_SERVICES_DIR / f"{service}.md",
            _service_page(
                service_dir,
                service_endpoint_docs.get(service, []),
                service in rest_only,
            ),
        )
    write_text_lf(DOCS_SERVICES_DIR / "index.md", _services_index_page(services))
    write_text_lf(
        DOCS_SERVICES_DIR / "README.md",
        _services_readme_page(services, service_endpoint_docs),
    )


def _group_by_tag(
    endpoint_docs: list[EndpointDoc],
) -> tuple[list[str], dict[str, list[EndpointDoc]]]:
    """Tags in first-seen order, and the endpoints under each."""
    grouped: dict[str, list[EndpointDoc]] = {}
    for doc in endpoint_docs:
        grouped.setdefault(doc.tag, []).append(doc)
    return list(grouped), grouped


def _service_page(
    service_dir: Path, endpoint_docs: list[EndpointDoc], rest_only: bool
) -> str:
    service = service_dir.name
    title = service.replace("_", " ").title()

    services_folder = service_dir / "services"
    if not services_folder.exists():
        services_folder = service_dir / "service"
    wrapper_file = (
        services_folder / f"{service}.py" if services_folder.exists() else None
    )
    wrapper_signatures = (
        parse_wrapper_method_signatures(wrapper_file)
        if wrapper_file and wrapper_file.exists()
        else {}
    )

    lines = [
        _provenance(render_endpoint_docs),
        f"<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->",
        "",
        f"# {title} Service",
        "",
    ]

    group_order, grouped = _group_by_tag(endpoint_docs)
    lines.extend(_render_service_overview(service, group_order, grouped, rest_only))
    lines.extend(["## Endpoints", ""])

    if not endpoint_docs:
        lines.extend(
            [
                "This service's schema defines shared types only. It has no REST endpoints.",
                "",
            ]
        )
    else:
        show_group_headers = len(group_order) > 1
        endpoint_heading_level = 4 if show_group_headers else 3
        for group_name in group_order:
            if show_group_headers:
                lines.extend([f"### {group_name}", ""])
            for idx, doc in enumerate(grouped[group_name]):
                if idx > 0:
                    lines.extend(["---", ""])
                lines.extend(
                    _render_endpoint_section(
                        service,
                        doc,
                        wrapper_signatures,
                        endpoint_heading_level,
                        rest_only,
                    )
                )

    lines.extend(["## Data Models", ""])
    models_dir = service_dir / "models"
    model_classes = sorted(discover_service_model_classes(service_dir))
    if not model_classes:
        lines.extend(["No data models for this service.", ""])
    else:
        lines.extend(
            _render_model_relationship_diagram(endpoint_docs, models_dir, model_classes)
        )
        for class_name in model_classes:
            directive = _autodoc_directive_for_model(models_dir, class_name)
            lines.extend(
                [
                    f"{MD_FENCE}{{eval-rst}}",
                    f".. {directive}:: kentik_api.gen.{service}.models.{class_name}",
                    *(["   :members:"] if directive == "autoclass" else []),
                    f"{MD_FENCE}",
                    "",
                ]
            )

    return "\n".join(lines)


def _services_index_page(services: list[str]) -> str:
    return (
        _provenance(render_endpoint_docs) + "\n"
        f"<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->\n\n"
        "# API Services\n\n"
        "For a runtime-level map of how the SDK client, mixin, auth/core/errors, "
        "and generated services connect, see "
        "[SDK Runtime Architecture](../sdk_runtime_architecture.md).\n\n"
        f"{MD_FENCE}{{toctree}}\n:maxdepth: 1\n\n"
        + "\n".join(sorted(services))
        + "\n"
        + f"{MD_FENCE}\n"
    )


def _services_readme_page(
    services: list[str], service_endpoint_docs: dict[str, list[EndpointDoc]]
) -> str:
    """services/README.md, built from the same data so it never goes stale."""
    readme_rows: list[str] = []
    for service in sorted(services):
        title = service.replace("_", " ").title()
        docs = service_endpoint_docs.get(service, [])
        blurb = next((d.summary for d in docs if d.summary), "")
        # Use space-content-space for filled cells; single space for empty ones so
        # markdownlint doesn't flag the double-space |  | pattern.
        desc_cell = f" {blurb} " if blurb else " "
        readme_rows.append(f"| {title} | [{service}.md]({service}.md) |{desc_cell}|")

    return "\n".join(
        [
            _provenance(render_endpoint_docs),
            f"<!-- Rebuilt on every `{REGENERATE_COMMAND}`. Do not edit by hand. -->",
            "",
            "# API Service Pages",
            "",
            "This folder holds one Markdown page per Kentik API service.",
            "[`scripts/generation/endpoint_docs.py`](../../scripts/generation/endpoint_docs.py) writes each page.",
            "",
            "> [!WARNING]",
            f"> Do not edit these files. Each `{REGENERATE_COMMAND}` run writes them again.",
            "",
            "## What each page contains",
            "",
            f"{MD_FENCE}text",
            "<service>.md",
            "├── Overview          the call path of the service, from your code to the Kentik API",
            "├── Endpoints         one section per operation",
            "│   ├── REST call flow    sequence diagram",
            "│   ├── gRPC call flow    sequence diagram, or why the operation has none",
            "│   ├── Parameters        name, location, type, and required flag",
            "│   ├── Responses         status, description, and model",
            "│   └── Example           a Python call to the operation",
            "└── Data Models       a model diagram, and the fields of each model",
            MD_FENCE,
            "",
            "## Services",
            "",
            "| Service | Page | Description |",
            "| --- | --- | --- |",
            *readme_rows,
            "",
        ]
    )


class EndpointDocsCollector:
    """Accumulates extract_endpoint_docs results, then renders them.

    Exists for callers that accumulate across a schema-availability loop;
    calling extract_endpoint_docs / render_endpoint_docs directly with a plain
    dict is equivalent. The ordering constraint (render() after wrapper
    generation) is the caller's responsibility, matching the module docstring.

    extract() deliberately does not catch exceptions: a swallowed failure
    publishes a silently empty page while the run reports success.
    """

    def __init__(self) -> None:
        self._docs: dict[str, list[EndpointDoc]] = {}

    def extract(self, service: str, swagger_path: Path) -> None:
        self._docs.setdefault(service, []).extend(extract_endpoint_docs(swagger_path))

    def write_record(self, path: Path = SCHEMA_RECORD_FILE) -> Path:
        """Writes each service's operations as the swagger declares them.

        Read straight from the schema, not from generated code, so a test can
        hold the generated modules to it without a schema checkout.
        """
        record = {
            service: {
                f"{doc.method} {doc.path}": {
                    "operation": doc.operation_id,
                    "params": sorted(param.name for param in doc.parameters),
                    "body": doc.request_body is not None,
                    "responses": sorted(resp.status for resp in doc.responses),
                }
                for doc in sorted(docs, key=lambda d: (d.path, d.method))
            }
            for service, docs in sorted(self._docs.items())
        }
        write_text_lf(path, json.dumps(record, indent=2) + "\n")
        return path

    def render(self, rest_only: frozenset[str] = frozenset()) -> None:
        render_endpoint_docs(self._docs, rest_only)
