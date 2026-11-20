# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Constants and helpers used by more than one generation phase module."""

import ast
import json
import keyword
import re
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SDK_OUTPUT_DIR = PROJECT_ROOT / "src" / "kentik_api" / "gen"

REGENERATE_COMMAND = "uv run poe generate"

INTERNAL_GEN_DIRS = frozenset({"__pycache__", "pb_companions"})

_MERMAID_FONT = "ui-monospace, SFMono-Regular, Menlo, monospace"

# The diagrams-skill palette, so sequence diagrams match the flowchart classes.
_MERMAID_THEME = {
    "fontFamily": _MERMAID_FONT,
    "primaryColor": "#f8f9fa",
    "primaryBorderColor": "#495057",
    "primaryTextColor": "#212529",
    "textColor": "#212529",
    "lineColor": "#77818c",
    "edgeLabelBackground": "#ffffff",
    "actorBkg": "#f8f9fa",
    "actorBorder": "#495057",
    "actorTextColor": "#212529",
    "actorLineColor": "#a9b3be",
    "signalColor": "#57616d",
    "signalTextColor": "#212529",
    "labelBoxBkgColor": "#f8f9fa",
    "labelBoxBorderColor": "#495057",
    "labelTextColor": "#212529",
    "loopTextColor": "#57616d",
    "noteBkgColor": "#fff9db",
    "noteBorderColor": "#f08c00",
    "noteTextColor": "#a35a00",
}


def mermaid_init() -> str:
    """The first line of a house-style Mermaid block.

    An init line, not YAML frontmatter: MyST reads a leading `---` block in a
    mermaid fence as directive options. Theme, look, layout and curve are
    Mermaid 12's defaults. themeVariables hold the light house colors, so
    diagram_assets/mermaid.css repaints the parts with the page tokens to
    follow the dark mode.
    """
    config = {
        "theme": "redux",
        "look": "neo",
        "layout": "elk",
        "fontFamily": _MERMAID_FONT,
        "themeVariables": _MERMAID_THEME,
        "sequence": {"activationWidth": 16},
        "flowchart": {
            "curve": "basis",
            "nodeSpacing": 30,
            "rankSpacing": 70,
            "wrappingWidth": 400,
        },
    }
    return f"%%{{init: {json.dumps(config)}}}%%"


def write_text_lf(path: Path, text: str) -> None:
    """Writes UTF-8 text with LF line endings on every OS.

    Path.write_text writes CRLF on Windows, and `git status` reports such a
    file as modified even under `eol=lf`, which fails the drift check.
    """
    path.write_bytes(text.encode("utf-8"))


def iter_service_dirs(root: Path | None = None) -> list[Path]:
    """Returns every generated Service directory under root, sorted by name.

    The one place that answers "is this directory a Service". A Service with no
    operations still counts: six exist today with models but no wrapper, and
    five of them are documented, so absence of a wrapper must not reclassify one
    as internal. Callers needing a wrapper should check for it separately.

    root resolves at call time, not at import time, so a caller that overrides
    its own SDK_OUTPUT_DIR (as the generator tests do) is honoured.
    """
    root = SDK_OUTPUT_DIR if root is None else root
    if not root.exists():
        return []
    return sorted(
        (p for p in root.iterdir() if p.is_dir() and p.name not in INTERNAL_GEN_DIRS),
        key=lambda p: p.name,
    )


def service_to_pascal_case(service: str) -> str:
    """Converts a snake_case service name to PascalCase."""
    return "".join(part.capitalize() for part in service.split("_") if part)


def normalize_symbol(symbol: str) -> str:
    """The Python name openapi-python-generator makes of a schema name.

    Mirrors its own normalize_symbol, so names derived here (path arguments,
    error classes) match the ones it writes into the REST modules.
    """
    name = re.sub(r"[^A-Za-z0-9_]", "", symbol.replace("-", "_").replace(" ", "_"))
    if keyword.iskeyword(name):
        name += "_"
    return "_" + name if name[:1].isdigit() else name


def discover_service_model_classes(service_dir: Path) -> set[str]:
    """Collects model class names generated for a service."""
    model_classes: set[str] = set()

    files_to_scan = (
        list((service_dir / "models").rglob("*.py"))
        if (service_dir / "models").exists()
        else []
    )
    if (service_dir / "models.py").exists():
        files_to_scan.append(service_dir / "models.py")

    for model_file in files_to_scan:
        model_classes.update(
            re.findall(
                r"^class ([A-Za-z0-9_]+)[\(:]", model_file.read_text(), re.MULTILINE
            )
        )

    return model_classes


@dataclass(frozen=True)
class GrpcCall:
    """The RPC a wrapper method calls on GrpcTransport, read from its source."""

    rpc: str  # "DeviceService/GetDevice"
    request: str  # "GetDeviceRequest"


def grpc_stub_services(init: ast.FunctionDef) -> dict[str, str]:
    """Maps each `self._grpc_stub_N` to its proto service, from `XStub(channel)`."""
    services = {}
    for sub in ast.walk(init):
        if (
            isinstance(sub, ast.Assign)
            and isinstance(sub.value, ast.Call)
            and isinstance(sub.value.func, ast.Attribute)
            and sub.value.func.attr.endswith("Stub")
        ):
            for target in sub.targets:
                if isinstance(target, ast.Attribute):
                    services[target.attr] = sub.value.func.attr.removesuffix("Stub")
    return services


def grpc_call(
    method: ast.FunctionDef, stub_services: dict[str, str]
) -> GrpcCall | None:
    """Reads `build_grpc_request(self._grpc_pb2_N.Req, ...)` and `call_grpc(self._grpc_stub_N.Rpc, ...)`.

    None means the method raises NotImplementedError on gRPC.
    """
    request = rpc = None
    for sub in ast.walk(method):
        if not (
            isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.args
        ):
            continue
        first = sub.args[0]
        if not isinstance(first, ast.Attribute):
            continue
        if sub.func.id == "build_grpc_request":
            request = first.attr
        elif (
            sub.func.id == "call_grpc"
            and isinstance(first.value, ast.Attribute)
            and first.value.attr in stub_services
        ):
            rpc = f"{stub_services[first.value.attr]}/{first.attr}"
    return GrpcCall(rpc=rpc, request=request) if rpc and request else None


@dataclass(frozen=True)
class RestOperation:
    """Parsed representation of one operation from a generated REST service module.

    Consumers:
    - tests/_discovery.py: uses http_method, expected_status, error_cls_name, operation_name
    - generation/endpoint_docs.py: uses http_method, path
    - generation/wrapper_generation.py: uses name, http_method, path, params,
      kwonly_start, return_type, query_params, docstring
    """

    name: str  # PascalCase function name
    http_method: str  # as written in source (e.g. "get", "post")
    path: str  # URL path template
    expected_status: int
    error_cls_name: str
    operation_name: str
    params: tuple[
        tuple[str, str, bool], ...
    ]  # (name, annotation, is_required) positional then kwonly
    kwonly_start: int  # params[:kwonly_start] are positional; the rest are keyword-only
    return_type: str  # annotation text as-is from the source
    query_params: tuple[tuple[str, str], ...]  # (wire name, argument name)
    docstring: str = ""  # the operation summary and description


def parse_generated_rest_module(path: Path) -> list[RestOperation]:
    """AST-parses a generated REST service module, returning one RestOperation per PascalCase function.

    Replaces three independent re-implementations in _discovery.py, endpoint_docs.py,
    and wrapper_generation.py. Skips functions without a request_json() call.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError:
        return []
    ops = (
        _rest_operation(node)
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name[:1].isupper()
    )
    return [op for op in ops if op is not None]


def _rest_operation(func: ast.FunctionDef) -> RestOperation | None:
    """The operation a REST function performs; None for a helper without request_json()."""
    kwargs = _request_json_keywords(func)
    method = kwargs.get("method")
    path = _path_template(kwargs.get("path"))
    if not isinstance(method, ast.Constant) or path is None:
        return None
    status = kwargs.get("expected_status")
    error_cls = kwargs.get("error_cls")
    operation = kwargs.get("operation_name")

    defaults_start = len(func.args.args) - len(func.args.defaults)
    positional = [
        (
            arg.arg,
            ast.unparse(arg.annotation) if arg.annotation else "Any",
            i < defaults_start,
        )
        for i, arg in enumerate(func.args.args)
    ]
    kwonly = [
        (
            arg.arg,
            ast.unparse(arg.annotation) if arg.annotation else "Any",
            default is None,
        )
        for arg, default in zip(func.args.kwonlyargs, func.args.kw_defaults)
    ]

    return RestOperation(
        name=func.name,
        http_method=str(method.value),
        path=path,
        expected_status=(
            status.value
            if isinstance(status, ast.Constant) and isinstance(status.value, int)
            else 0
        ),
        error_cls_name=error_cls.id if isinstance(error_cls, ast.Name) else "",
        operation_name=(
            str(operation.value) if isinstance(operation, ast.Constant) else ""
        )
        or func.name,
        params=tuple(positional + kwonly),
        kwonly_start=len(positional),
        return_type=ast.unparse(func.returns) if func.returns else "",
        query_params=_query_params(func),
        docstring=ast.get_docstring(func) or "",
    )


def _request_json_keywords(func: ast.FunctionDef) -> dict[str, ast.expr]:
    """The keyword arguments of a function's request_json() call; {} without one."""
    call = next(
        (
            sub
            for sub in ast.walk(func)
            if isinstance(sub, ast.Call)
            and isinstance(sub.func, ast.Name)
            and sub.func.id == "request_json"
        ),
        None,
    )
    return {kw.arg: kw.value for kw in call.keywords if kw.arg} if call else {}


def _path_template(value: ast.expr | None) -> str | None:
    """A request_json() path as a template: {path_segment(deviceid)} reads {deviceid}."""
    if isinstance(value, ast.Constant):
        return str(value.value)
    if not isinstance(value, ast.JoinedStr):
        return None
    parts: list[str] = []
    for part in value.values:
        if isinstance(part, ast.Constant):
            parts.append(str(part.value))
        elif isinstance(part, ast.FormattedValue):
            arg = part.value
            if (
                isinstance(arg, ast.Call)
                and isinstance(arg.func, ast.Name)
                and arg.func.id == "path_segment"
            ):
                arg = arg.args[0]
            parts.append(f"{{{ast.unparse(arg)}}}")
    return "".join(parts)


def _query_params(func: ast.FunctionDef) -> tuple[tuple[str, str], ...]:
    """(wire name, argument name) per query parameter of a REST function.

    The wire name keeps the dotted field path ("pagination.limit") that the
    argument name ("paginationlimit") loses.
    """
    return next(
        (
            tuple(
                (str(key.value), value.id)
                for key, value in zip(stmt.value.keys, stmt.value.values)
                if isinstance(key, ast.Constant) and isinstance(value, ast.Name)
            )
            for stmt in func.body
            if isinstance(stmt, ast.AnnAssign)
            and isinstance(stmt.target, ast.Name)
            and stmt.target.id == "query_params"
            and isinstance(stmt.value, ast.Dict)
        ),
        (),
    )


@dataclass(frozen=True)
class WrapperMethod:
    """Parsed representation of one method from a generated *ServiceWrapper class.

    Consumers:
    - generation/docs_rendering.py: uses name, params, return_type, has_data_param
    - generation/endpoint_docs.py: uses name, params, kwonly_start for required flags
    """

    name: str
    params: tuple[
        tuple[str, str, bool], ...
    ]  # (name, annotation, is_required) positional then kwonly
    kwonly_start: int
    return_type: str
    has_data_param: bool  # True if any kwonly param is named "data"


def parse_wrapper_methods(path: Path) -> list[WrapperMethod]:
    """AST-parses a *ServiceWrapper file and returns one WrapperMethod per public method.

    Skips __init__ and any method starting with '_'. Symmetric with
    parse_generated_rest_module for REST service files.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError:
        return []

    wrapper_class: ast.ClassDef | None = None
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name.endswith("ServiceWrapper"):
            wrapper_class = node
            break
    if wrapper_class is None:
        return []

    methods: list[WrapperMethod] = []
    for node in wrapper_class.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue

        return_type = ast.unparse(node.returns) if node.returns else ""

        defaults_start = len(node.args.args) - len(node.args.defaults)
        positional: list[tuple[str, str, bool]] = [
            (
                arg.arg,
                ast.unparse(arg.annotation) if arg.annotation else "Any",
                i < defaults_start,
            )
            for i, arg in enumerate(node.args.args)
            if arg.arg != "self"
        ]
        kwonly: list[tuple[str, str, bool]] = [
            (
                arg.arg,
                ast.unparse(arg.annotation) if arg.annotation else "Any",
                default is None,
            )
            for arg, default in zip(node.args.kwonlyargs, node.args.kw_defaults)
        ]
        all_params = tuple(positional + kwonly)
        has_data = any(name == "data" for name, _, _ in all_params)

        methods.append(
            WrapperMethod(
                name=node.name,
                params=all_params,
                kwonly_start=len(positional),
                return_type=return_type,
                has_data_param=has_data,
            )
        )

    return methods
