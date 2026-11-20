# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Unit tests for parse_wrapper_method_signatures, parse_wrapper_methods, and render_endpoint_docs."""

import ast
import importlib
import re
from pathlib import Path

import pytest

from scripts.generation._shared import parse_wrapper_methods
from scripts.generation.endpoint_docs import (
    EndpointDoc,
    EndpointDocsCollector,
    GrpcCall,
    _example_value_for_annotation,
    _nest_headings,
    _provenance,
    _render_example_snippet,
    _render_operation_sequence_diagram,
    parse_wrapper_method_signatures,
    render_endpoint_docs,
)

_REST_MODULE = """\
from typing import Optional
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from ..error import ListThingsError, GetThingError

def ListThings(
    api_config_override: Optional[APIConfig] = None,
) -> ListThingsResponse:
    body = request_json(
        method="get",
        path="/things/v1/thing",
        api_config_override=api_config_override,
        expected_status=200,
        operation_name="ListThings",
        error_cls=ListThingsError,
    )
    return ListThingsResponse(**body)


def GetThing(
    api_config_override: Optional[APIConfig] = None,
    *,
    thing_id: str,
) -> GetThingResponse:
    body = request_json(
        method="get",
        path=f"/things/v1/thing/{path_segment(thing_id)}",
        api_config_override=api_config_override,
        expected_status=200,
        operation_name="GetThing",
        error_cls=GetThingError,
    )
    return GetThingResponse(**body)
"""


def _make_wrapper(services_dir: Path, service: str, rest_stem: str) -> Path:
    """Writes a minimal ServiceWrapper file that mirrors the REST module fixture."""
    title = "".join(p.capitalize() for p in service.split("_"))
    wrapper = services_dir / f"{service}.py"
    wrapper.write_text(
        f"import kentik_api.gen.{service}.services.{rest_stem} as Rest{title}Module1\n"
        f"\n"
        f"class {title}ServiceWrapper:\n"
        f"    def __init__(self, transport):\n"
        f"        self._transport = transport\n"
        f"\n"
        f"    def list_things(self) -> ListThingsResponse:\n"
        f"        return Rest{title}Module1.ListThings()\n"
        f"\n"
        f"    def get_thing(self, *, thing_id: str) -> GetThingResponse:\n"
        f"        return Rest{title}Module1.GetThing(thing_id=thing_id)\n",
        encoding="utf-8",
    )
    return wrapper


def test_parse_wrapper_method_signatures_maps_list_operation(tmp_path: Path) -> None:
    svc = tmp_path / "services"
    svc.mkdir()
    rest_file = svc / "ThingService.py"
    rest_file.write_text(_REST_MODULE, encoding="utf-8")
    wrapper = _make_wrapper(svc, "thing", "ThingService")

    result = parse_wrapper_method_signatures(wrapper)

    assert ("GET", "/things/v1/thing") in result
    method_name, params, grpc_call = result[("GET", "/things/v1/thing")]
    assert method_name == "list_things"
    assert params == []  # list_things takes no params besides self
    assert grpc_call is None  # the fixture wrapper has no gRPC branch


def test_parse_wrapper_method_signatures_maps_get_with_path_param(
    tmp_path: Path,
) -> None:
    svc = tmp_path / "services"
    svc.mkdir()
    rest_file = svc / "ThingService.py"
    rest_file.write_text(_REST_MODULE, encoding="utf-8")
    wrapper = _make_wrapper(svc, "thing", "ThingService")

    result = parse_wrapper_method_signatures(wrapper)

    assert ("GET", "/things/v1/thing/{thing_id}") in result
    method_name, params, _ = result[("GET", "/things/v1/thing/{thing_id}")]
    assert method_name == "get_thing"
    assert any(p[0] == "thing_id" for p in params)


def test_parse_wrapper_method_signatures_reads_the_rpc_each_method_calls(
    tmp_path: Path,
) -> None:
    svc = tmp_path / "services"
    svc.mkdir()
    (svc / "ThingService.py").write_text(_REST_MODULE, encoding="utf-8")
    wrapper = svc / "thing.py"
    wrapper.write_text(
        "import kentik_api.gen.thing.services.ThingService as RestThingModule1\n"
        "\n"
        "class ThingServiceWrapper:\n"
        "    def __init__(self, transport):\n"
        "        self._grpc_stub_1 = _grpc_1_mod.ThingAdminServiceStub(transport.channel)\n"
        "\n"
        "    def get_thing(self, *, thing_id: str) -> GetThingResponse:\n"
        "        if grpc:\n"
        "            _req = build_grpc_request(self._grpc_pb2_1.GetThingRequest, None, {})\n"
        "            _resp, _ = call_grpc(self._grpc_stub_1.GetThing, _req)\n"
        "        return RestThingModule1.GetThing(thing_id=thing_id)\n",
        encoding="utf-8",
    )

    _, _, grpc_call = parse_wrapper_method_signatures(wrapper)[
        ("GET", "/things/v1/thing/{thing_id}")
    ]

    assert grpc_call == GrpcCall(
        rpc="ThingAdminService/GetThing", request="GetThingRequest"
    )


def test_parse_wrapper_method_signatures_returns_empty_without_wrapper_class(
    tmp_path: Path,
) -> None:
    wrapper = tmp_path / "no_wrapper.py"
    wrapper.write_text("# no class here\n", encoding="utf-8")
    assert parse_wrapper_method_signatures(wrapper) == {}


def test_parse_wrapper_method_signatures_skips_init(tmp_path: Path) -> None:
    svc = tmp_path / "services"
    svc.mkdir()
    rest_file = svc / "ThingService.py"
    rest_file.write_text(_REST_MODULE, encoding="utf-8")
    wrapper = _make_wrapper(svc, "thing", "ThingService")

    result = parse_wrapper_method_signatures(wrapper)

    for method_name, _, _ in result.values():
        assert method_name != "__init__"


_WRAPPER_FIXTURE = """\
import kentik_api.gen.thing.services.ThingService as RestThingModule1

class ThingServiceWrapper:
    def __init__(self, transport):
        self._transport = transport

    def list_things(self) -> rest_models.ListThingsResponse:
        return RestThingModule1.ListThings()

    def create_thing(self, *, data: rest_models.CreateThingRequest) -> rest_models.CreateThingResponse:
        return RestThingModule1.CreateThing(data=data)

    def _private(self):
        pass
"""


def test_parse_wrapper_methods_returns_public_methods(tmp_path: Path) -> None:
    f = tmp_path / "thing.py"
    f.write_text(_WRAPPER_FIXTURE, encoding="utf-8")
    methods = parse_wrapper_methods(f)
    names = [m.name for m in methods]
    assert "list_things" in names
    assert "create_thing" in names
    assert "__init__" not in names
    assert "_private" not in names


def test_parse_wrapper_methods_detects_data_param(tmp_path: Path) -> None:
    f = tmp_path / "thing.py"
    f.write_text(_WRAPPER_FIXTURE, encoding="utf-8")
    methods = {m.name: m for m in parse_wrapper_methods(f)}
    assert not methods["list_things"].has_data_param
    assert methods["create_thing"].has_data_param


def test_parse_wrapper_methods_extracts_return_type(tmp_path: Path) -> None:
    f = tmp_path / "thing.py"
    f.write_text(_WRAPPER_FIXTURE, encoding="utf-8")
    methods = {m.name: m for m in parse_wrapper_methods(f)}
    assert "ListThingsResponse" in methods["list_things"].return_type


def test_parse_wrapper_methods_empty_without_class(tmp_path: Path) -> None:
    f = tmp_path / "empty.py"
    f.write_text("# nothing\n", encoding="utf-8")
    assert parse_wrapper_methods(f) == []


def test_provenance_names_a_function_that_resolves():
    """Guards the defect where 42 pages named a function that did not exist.

    Asserts resolvability rather than a fixed string, so renaming the writer
    cannot leave the header stale without this failing.
    """
    header = _provenance(render_endpoint_docs)

    assert header.startswith("<!-- AUTO-GENERATED: ")
    inner = header.removeprefix("<!-- AUTO-GENERATED: ").removesuffix(" -->")
    module_rel, func_part = (part.strip() for part in inner.split(",", 1))
    func_name = func_part.removesuffix("()")

    project_root = Path(__file__).resolve().parents[2]
    module_file = project_root / module_rel
    assert module_file.exists(), f"provenance names a missing module: {module_rel}"

    source = module_file.read_text(encoding="utf-8")
    assert f"def {func_name}(" in source, (
        f"provenance names {func_name}(), which does not exist in {module_rel}"
    )


def test_provenance_tracks_a_rename():
    """A differently-named writer must produce a differently-named header."""

    def some_other_writer() -> None:  # pragma: no cover - name only
        pass

    assert "some_other_writer()" in _provenance(some_other_writer)


def test_extract_propagates_failure_instead_of_swallowing_it(tmp_path: Path):
    """A swallowed failure yields a silently empty page while the run succeeds.

    Same shape as the None-return that erased the gRPC runtime from the
    architecture diagram with no error anywhere.
    """
    unparseable = tmp_path / "broken.swagger.json"
    unparseable.write_text("{ this is not json", encoding="utf-8")

    collector = EndpointDocsCollector()

    with pytest.raises(ValueError, match="Expecting"):
        collector.extract("broken_service", unparseable)


import json  # noqa: E402

_REPO = Path(__file__).resolve().parents[2]
_COMMITTED_PAGES = _REPO / "docs" / "sphinx" / "services"

_DEFAULT_ERROR = {
    "description": "An unexpected error response.",
    "content": {
        "application/json": {"schema": {"$ref": "#/components/schemas/rpcStatus"}}
    },
}


def _ok(schema: str) -> dict:
    return {
        "description": "A successful response.",
        "content": {
            "application/json": {"schema": {"$ref": f"#/components/schemas/{schema}"}}
        },
    }


_DEVICE_SWAGGER = {
    "openapi": "3.0.1",
    "tags": [{"name": "DeviceService"}],
    "paths": {
        "/device/v202504beta2/device": {
            "get": {
                "operationId": "ListDevices",
                "summary": "List all devices.",
                "description": "Returns list of configured devices. Use the 'view' parameter to control response detail: FULL (default), BASIC (id, name, status), or ID_ONLY (id only). See [About Devices](https://kb.kentik.com/v4/Cb01.htm).",
                "parameters": [
                    {
                        "name": "query.noCustomColumns",
                        "in": "query",
                        "schema": {"type": "boolean"},
                    },
                    {"name": "view", "in": "query", "schema": {"type": "string"}},
                ],
                "responses": {
                    "200": _ok("ListDevicesResponse"),
                    "default": _DEFAULT_ERROR,
                },
            },
            "post": {
                "operationId": "CreateDevice",
                "summary": "Configure a new device.",
                "description": "Create configuration for a new device. Returns the newly created configuration (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/CreateDeviceRequest"
                            }
                        }
                    },
                },
                "responses": {
                    "200": _ok("CreateDeviceResponse"),
                    "default": _DEFAULT_ERROR,
                },
            },
        },
        "/device/v202504beta2/device/{device.id}": {
            "get": {
                "operationId": "GetDevice",
                "summary": "Retrieve configuration of a device.",
                "description": "Returns configuration of a device specified by ID (see [About Devices](https://kb.kentik.com/v4/Cb01.htm)).",
                "parameters": [
                    {
                        "name": "device.id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    },
                    {
                        "name": "query.noCustomColumns",
                        "in": "query",
                        "schema": {"type": "boolean"},
                    },
                ],
                "responses": {
                    "200": _ok("GetDeviceResponse"),
                    "default": _DEFAULT_ERROR,
                },
            }
        },
    },
}


def _alerting_swagger(path: str, tag: str) -> dict:
    return {
        "openapi": "3.0.1",
        "tags": [{"name": tag}],
        "paths": {
            path: {
                "post": {
                    "operationId": "List",
                    "summary": f"{tag} list.",
                    "responses": {
                        "200": _ok("SomeResponse"),
                        "default": _DEFAULT_ERROR,
                    },
                }
            }
        },
    }


def _write(tmp_path: Path, name: str, swagger: dict) -> Path:
    path = tmp_path / "swagger" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(swagger))
    return path


def _section(page: str, heading: str) -> str:
    """One endpoint section, at whatever level it renders.

    Single-tag services use `###` and `---` separators; multi-tag services nest
    endpoints under a tag heading at `####` with no separator. So a section ends
    at a separator or at the next heading of the same or higher level.
    """
    lines = page.splitlines(keepends=True)
    start = next(
        i for i, line in enumerate(lines) if line.lstrip("#") == heading.lstrip("#")
    )
    level = len(lines[start]) - len(lines[start].lstrip("#"))
    end = len(lines)
    in_fence = False
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("```"):
            in_fence = not in_fence
        if in_fence:
            continue  # a `#` comment in an example is not a heading
        hashes = len(lines[i]) - len(lines[i].lstrip("#"))
        if lines[i] == "---\n" or 0 < hashes <= level:
            end = i
            break
    return "".join(lines[start:end]).rstrip("\n")


def _without_provenance(page: str) -> str:
    return page.split("\n", 1)[1]


def _model_directives(page: str) -> set[str]:
    return {line for line in page.splitlines() if line.startswith(".. auto")}


@pytest.fixture
def rendered(sandbox, tmp_path) -> Path:
    collector = EndpointDocsCollector()
    collector.extract("device", _write(tmp_path, "device.json", _DEVICE_SWAGGER))
    collector.extract(
        "alerting",
        _write(
            tmp_path,
            "ack.json",
            _alerting_swagger("/v202505/alerts/ack/auto/list", "AlertAutoAckService"),
        ),
    )
    collector.extract(
        "alerting",
        _write(
            tmp_path,
            "alerts.json",
            _alerting_swagger("/v202505/alerts", "AlertService"),
        ),
    )
    collector.extract(
        "alerting", _write(tmp_path, "empty.json", {"openapi": "3.0.1", "paths": {}})
    )
    stale = sandbox.docs / "services" / "retired_service.md"
    stale.parent.mkdir(parents=True, exist_ok=True)
    stale.write_text("left over from a service that no longer exists")

    collector.render()
    return sandbox.docs / "services"


@pytest.mark.parametrize(
    "heading",
    [
        "### `GET` `/device/v202504beta2/device`\n",
        "### `POST` `/device/v202504beta2/device`\n",
        "### `GET` `/device/v202504beta2/device/{device.id}`\n",
    ],
)
def test_endpoint_sections_match_the_committed_page_exactly(rendered, heading):
    produced = (rendered / "device.md").read_text()
    committed = (_COMMITTED_PAGES / "device.md").read_text()

    assert _section(produced, heading) == _section(committed, heading)


def test_every_model_gets_the_same_directive_as_the_committed_page(rendered):
    produced = (rendered / "device.md").read_text()
    committed = (_COMMITTED_PAGES / "device.md").read_text()

    assert _model_directives(produced) == _model_directives(committed)


def test_enum_models_use_autoclass_and_pydantic_models_use_autopydantic(rendered):
    page = (rendered / "device.md").read_text()

    assert ".. autoclass:: kentik_api.gen.device.models.DeviceView" in page
    assert (
        ".. autopydantic_model:: kentik_api.gen.device.models.CreateDeviceRequest"
        in page
    )


def test_service_without_endpoints_matches_the_committed_page(rendered):
    produced = (rendered / "core.md").read_text()

    assert _without_provenance(produced) == _without_provenance(
        (_COMMITTED_PAGES / "core.md").read_text()
    )


def test_reused_operation_ids_resolve_to_the_right_wrapper_method(rendered):
    page = (rendered / "alerting.md").read_text()

    ack = _section(page, "### `POST` `/v202505/alerts/ack/auto/list`\n")
    alerts = _section(page, "### `POST` `/v202505/alerts`\n")
    assert "client.alerting.auto_ack_list(" in ack
    assert "client.alerting.list(" in alerts
    assert "client.alerting.list(" not in ack


def test_render_removes_pages_for_services_that_no_longer_exist(rendered):
    assert not (rendered / "retired_service.md").exists()
    assert {p.stem for p in rendered.glob("*.md")} >= {
        "device",
        "alerting",
        "core",
        "index",
    }


def test_services_index_lists_every_sandbox_service(rendered):
    index = (rendered / "index.md").read_text()

    for service in ("alerting", "core", "device"):
        assert f"\n{service}\n" in index


_PRIMITIVE_LABELS = {"-", "string", "boolean", "integer", "number", "object"}


@pytest.mark.parametrize(
    "page",
    sorted(
        p for p in _COMMITTED_PAGES.glob("*.md") if p.stem not in {"index", "README"}
    ),
    ids=lambda p: p.stem,
)
def test_every_model_a_committed_page_names_exists_in_the_sdk(page):
    defined = {
        p.stem
        for p in (_REPO / "src/kentik_api/gen" / page.stem / "models").glob("*.py")
    }
    labels = re.findall(r"\| `([A-Za-z0-9_]+)(?:\[\])?` \|\n", page.read_text())

    assert {label for label in labels if label not in _PRIMITIVE_LABELS} <= defined


@pytest.mark.parametrize(
    "page",
    sorted(
        p for p in _COMMITTED_PAGES.glob("*.md") if p.stem not in {"index", "README"}
    ),
    ids=lambda p: p.stem,
)
def test_every_committed_example_imports_what_it_uses(page):
    for snippet in re.findall(r"```python\n(.*?)```", page.read_text(), re.DOTALL):
        tree = ast.parse(snippet)
        bound = {"response", "client"}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = importlib.import_module(node.module or "")
                for alias in node.names:
                    assert hasattr(module, alias.name), f"{node.module}.{alias.name}"
                    bound.add(alias.name)
        used = {
            n.id
            for n in ast.walk(tree)
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)
        }

        assert used <= bound, snippet


@pytest.mark.parametrize(
    ("annotation", "value", "models"),
    [
        ("Dict[str, Any]", "{}", set()),
        ("Optional[List[rest_models.Label]]", "[Label(...)]", {"Label"}),
    ],
)
def test_example_value_names_only_constructible_models(annotation, value, models):
    found: set[str] = set()

    assert _example_value_for_annotation(annotation, "x", found) == value
    assert found == models


def test_a_rest_only_service_documents_rest_for_both_protocols():
    doc = EndpointDoc(
        tag="QueryService",
        method="POST",
        path="/query/topXdata",
        operation_id="QueryService_TopXData",
        summary="",
        description="",
        parameters=[],
        request_body=None,
        responses=[],
    )

    snippet = _render_example_snippet("v5", "top_x_data", [], rest_only=True)
    diagram = "\n".join(
        _render_operation_sequence_diagram(
            "v5", doc, "top_x_data", [], None, "####", rest_only=True
        )
    )

    assert "REST only" in snippet
    assert "Both transports work" not in snippet
    assert "also sends this call over REST" in diagram
    assert "NotImplementedError" not in diagram


def test_description_headings_nest_under_the_endpoint():
    text = "Intro\n### Fields\n#### Detail\n```\n# not a heading\n```\n### Examples"

    assert _nest_headings(text, 5) == (
        "Intro\n##### Fields\n###### Detail\n```\n# not a heading\n```\n##### Examples"
    )
    assert _nest_headings("No headings", 5) == "No headings"
