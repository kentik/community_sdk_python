# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Tests for scripts/generation/api_surface.py.

Builds surface dicts directly rather than generating an SDK, so these stay offline
and fast. capture() itself is covered against a minimal fixture tree.
"""

from __future__ import annotations

from pathlib import Path

from scripts.generation import api_surface


def _surface(services: dict, **top) -> dict:
    return {
        "schema_version": 1,
        "requirements": top.get("requirements", {}),
        "gencode": top.get("gencode", {}),
        "services": services,
    }


def _service(operations=(), models=(), mounted=True, fields=None, enums=None) -> dict:
    return {
        "mounted": mounted,
        "operations": {
            op: {"operation": op.split()[-1], "status": 200} for op in operations
        },
        "models": list(models),
        "fields": fields or {},
        "enums": enums or {},
    }


def _field(type_="Optional[str]", required=False) -> dict:
    return {"type": type_, "required": required}


def _render(before: dict, after: dict) -> str:
    return api_surface.render_markdown(api_surface.diff(before, after), since="v1.0.7")


def test_identical_surfaces_produce_no_delta():
    surface = _surface({"device": _service(["GET /device"], ["Device"])})

    delta = api_surface.diff(surface, surface)

    assert api_surface.is_empty(delta)
    assert "No public API surface changes" in api_surface.render_markdown(
        delta, since="v1.0.7"
    )


def test_added_service_is_reported_with_its_operations():
    before = _surface({})
    after = _surface({"kmeta": _service(["GET /kmeta/config"], ["ServiceNowConfig"])})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert "### New services" in markdown
    assert "**kmeta** (`client.kmeta`)" in markdown
    assert "`GET /kmeta/config`" in markdown
    assert "Breaking changes" not in markdown


def test_unmounted_service_is_labelled_types_only():
    after = _surface({"kptr": _service([], ["PtrResult"], mounted=False)})

    markdown = api_surface.render_markdown(
        api_surface.diff(_surface({}), after), since="v1.0.7"
    )

    assert "types only, not mounted on the client" in markdown


def test_removed_operation_is_flagged_breaking():
    before = _surface({"device": _service(["GET /device", "POST /device"])})
    after = _surface({"device": _service(["GET /device"])})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert markdown.startswith("### Breaking changes")
    assert "`device`: operation removed, `POST /device`" in markdown


def test_removed_service_is_flagged_breaking():
    before = _surface({"vault": _service(["GET /secrets"])})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, _surface({})), since="v1.0.7"
    )

    assert "Service removed: `client.vault`" in markdown


def test_unmounting_a_service_is_flagged_breaking():
    before = _surface({"ktbgp": _service(["POST /routes/list"], mounted=True)})
    after = _surface({"ktbgp": _service(["POST /routes/list"], mounted=False)})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert "`client.ktbgp` is no longer available" in markdown


def test_new_required_dependency_is_flagged_breaking():
    before = _surface({}, requirements={"grpcio": "grpcio>=1.78.0"})
    after = _surface(
        {}, requirements={"grpcio": "grpcio>=1.84.0", "protobuf": "protobuf>=7.35.1,<8"}
    )

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert "New required dependency, `protobuf>=7.35.1,<8`" in markdown
    assert (
        "Dependency requirement narrowed, `grpcio>=1.78.0` to `grpcio>=1.84.0`"
        in markdown
    )


def _requirement_breaks(before: str, after: str) -> bool:
    current = {"schema_version": api_surface.SCHEMA_VERSION}
    delta = api_surface.diff(
        {**_surface({}, requirements={"pkg": before}), **current},
        {**_surface({}, requirements={"pkg": after}), **current},
    )
    return bool(api_surface.breaking_changes(delta))


def test_loosened_requirement_is_not_breaking():
    assert not _requirement_breaks("httpx>=0.28.1,<1", "httpx>=0.27,<2")
    assert not _requirement_breaks("httpx<1,>=0.28.1", "httpx>=0.28.1")


def test_narrowed_requirement_is_breaking():
    assert _requirement_breaks("httpx>=0.28.1", "httpx>=0.28.1,<1")
    assert _requirement_breaks("httpx>=0.28.1,<2", "httpx>=0.28.1,<1")
    assert _requirement_breaks("httpx>=0.28.1", "httpx>=0.28.1,!=0.29.0")
    assert _requirement_breaks("httpx>=0.28.1", "httpx[http2]>=0.28.1")


def test_record_tracks_every_dependency_and_python_floor():
    requirements = api_surface._declared_requirements()

    assert {"python-dotenv", "googleapis-common-protos", "python"} <= set(requirements)
    assert requirements["python"].startswith("python>=")


def test_older_record_does_not_report_untracked_dependencies_as_new():
    before = _surface({}, requirements={"httpx": "httpx>=0.28.1"})
    after = {
        **_surface(
            {}, requirements={"httpx": "httpx>=0.28.1", "python": "python>=3.12"}
        ),
        "schema_version": api_surface.SCHEMA_VERSION,
    }

    assert api_surface.diff(before, after)["requirements"] == {}


def test_gencode_bump_is_reported_but_not_breaking():
    before = _surface({}, gencode={"protobuf": "6.33.5"})
    after = _surface({}, gencode={"protobuf": "7.35.1"})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert "`protobuf` gencode: `6.33.5` to `7.35.1`" in markdown
    assert "Breaking changes" not in markdown


def test_operations_are_keyed_by_method_and_path_not_operation_id():
    """Multi-file services reuse generic operation ids such as `List`."""
    before = _surface({"alerting": _service(["GET /alerts", "GET /mitigations"])})
    after = _surface({"alerting": _service(["GET /alerts"])})

    delta = api_surface.diff(before, after)

    assert delta["changed_services"]["alerting"]["removed_operations"] == [
        "GET /mitigations"
    ]


def test_capture_reads_a_generated_tree(tmp_path: Path):
    service = tmp_path / "demo"
    (service / "services").mkdir(parents=True)
    (service / "models").mkdir()
    (service / "models" / "Thing.py").write_text(
        "class Thing(BaseModel):\n"
        '    model_config = {"populate_by_name": True}\n'
        '    name: str = Field(validation_alias="name")\n'
        '    note: Optional[str] = Field(validation_alias="note", default=None)\n'
    )
    (service / "models" / "Color.py").write_text(
        'class Color(str, Enum):\n    RED = "RED"\n    BLUE = "BLUE"\n'
    )
    (service / "services" / "DemoService.py").write_text(
        "from kentik_api.core.rest_runtime import request_json\n"
        "def ListThings(*, cid: str) -> Thing:\n"
        "    return request_json(\n"
        '        method="get",\n'
        '        path=f"/demo/v1/{path_segment(cid)}/things",\n'
        "        expected_status=200,\n"
        "        error_cls=DemoError,\n"
        '        operation_name="ListThings",\n'
        "    )\n"
    )
    (service / "services" / "demo.py").write_text(
        "import kentik_api.gen.demo.services.DemoService as RestDemoModule1\n"
        "class DemoServiceWrapper:\n"
        "    def list_things(self, *, cid):\n"
        "        return RestDemoModule1.ListThings(cid=cid)\n"
    )

    surface = api_surface.capture(tmp_path)

    demo = surface["services"]["demo"]
    assert demo["models"] == ["Color", "Thing"]
    assert demo["fields"] == {
        "Thing": {
            "name": {"type": "str", "required": True},
            "note": {"type": "Optional[str]", "required": False},
        }
    }
    assert demo["enums"] == {"Color": ["RED", "BLUE"]}
    operations = surface["services"]["demo"]["operations"]
    assert "GET /demo/v1/{cid}/things" in operations
    assert operations["GET /demo/v1/{cid}/things"]["operation"] == "ListThings"
    assert operations["GET /demo/v1/{cid}/things"]["required_params"] == ["cid"]
    assert operations["GET /demo/v1/{cid}/things"]["method"] == "list_things"
    assert operations["GET /demo/v1/{cid}/things"]["grpc"] is None


def test_capture_flags_services_mounted_on_the_v5_transport(
    tmp_path: Path, monkeypatch
):
    for name in ("v5", "device"):
        (tmp_path / "gen" / name / "services").mkdir(parents=True)
    mixin = tmp_path / "src" / "kentik_api" / "client_mixin.py"
    mixin.parent.mkdir(parents=True)
    mixin.write_text(
        "from kentik_api.gen.device.services.device import DeviceServiceWrapper\n"
        "from kentik_api.gen.v5.services.v5 import V5ServiceWrapper\n"
        "        self.device = DeviceServiceWrapper(self._transport)\n"
        "        self.v5 = V5ServiceWrapper(self._v5_transport)\n"
    )
    (tmp_path / "pyproject.toml").write_text("[project]\ndependencies = []\n")
    monkeypatch.setattr(api_surface, "PROJECT_ROOT", tmp_path)

    surface = api_surface.capture(tmp_path / "gen")

    assert surface["schema_version"] == 8
    assert api_surface.is_rest_only(surface["services"]["v5"])
    assert not api_surface.is_rest_only(surface["services"]["device"])


def test_a_record_before_schema_version_8_has_no_rest_only_service():
    assert not api_surface.is_rest_only(_service())


def test_capture_records_the_rpc_each_wrapper_method_calls(tmp_path: Path):
    service = tmp_path / "demo"
    (service / "services").mkdir(parents=True)
    (service / "services" / "DemoService.py").write_text(
        "def ListThings() -> None:\n"
        '    return request_json(method="get", path="/things", expected_status=200)\n'
    )
    (service / "services" / "demo.py").write_text(
        "import kentik_api.gen.demo.services.DemoService as RestDemoModule1\n"
        "class DemoServiceWrapper:\n"
        "    def __init__(self, transport):\n"
        "        self._grpc_stub_1 = pb2_grpc.DemoServiceStub(transport.channel)\n"
        "    def list_things(self):\n"
        "        if grpc:\n"
        "            _req = build_grpc_request(self._grpc_pb2_1.ListThingsRequest, None, {})\n"
        "            return call_grpc(self._grpc_stub_1.ListThings, _req)\n"
        "        return RestDemoModule1.ListThings()\n"
    )

    surface = api_surface.capture(tmp_path)

    operation = surface["services"]["demo"]["operations"]["GET /things"]
    assert operation["grpc"] == "DemoService/ListThings"


def _routed(route: str | None) -> dict:
    surface = _surface({"demo": _service(["GET /thing"])})
    surface["services"]["demo"]["operations"]["GET /thing"]["grpc"] = route
    return surface


def test_a_lost_grpc_route_is_breaking_and_a_new_one_is_not():
    routed, unrouted = _routed("DemoService/Get"), _routed(None)

    lost = api_surface.breaking_changes(api_surface.diff(routed, unrouted))
    gained = api_surface.breaking_changes(api_surface.diff(unrouted, routed))

    assert lost == [
        (
            "- `demo`: `GET /thing` no longer routes to gRPC `DemoService/Get`",
            "DemoService/Get",
        )
    ]
    assert gained == []
    assert "`GET /thing` routes to gRPC `DemoService/Get`" in _render(unrouted, routed)


def test_a_record_without_grpc_routes_compares_as_unchanged():
    """Records written before schema_version 5 carry no gRPC routes."""
    before = _surface({"demo": _service(["GET /thing"])})

    assert api_surface.is_empty(api_surface.diff(before, _routed("DemoService/Get")))


def test_capture_records_each_operation_error_class(tmp_path: Path):
    service = tmp_path / "demo"
    (service / "services").mkdir(parents=True)
    (service / "error").mkdir()
    (service / "services" / "DemoService.py").write_text(
        "def ListThings() -> None:\n"
        '    return request_json(method="get", path="/things", expected_status=200,\n'
        "        error_cls=ListThingsError)\n"
    )
    (service / "error" / "__init__.py").write_text(
        "class ListThingsError(DemoError): ...\n"
        "class ListThingsNotFoundError(ListThingsError): ...\n"
        'ListThingsError.response_error_map = {"404": ListThingsNotFoundError}\n'
    )

    operation = api_surface.capture(tmp_path)["services"]["demo"]["operations"][
        "GET /things"
    ]

    assert operation["error"] == "ListThingsError"
    assert operation["error_responses"] == {"404": "ListThingsNotFoundError"}


def _raising(error: str, **responses: str) -> dict:
    surface = _surface({"demo": _service(["GET /thing"])})
    operation = surface["services"]["demo"]["operations"]["GET /thing"]
    operation.update(error=error, error_responses=responses)
    return surface


def test_a_renamed_error_class_is_breaking():
    before = _raising("GetThingError", **{"404": "GetThingNotFoundError"})
    after = _raising("ThingGetError", **{"404": "ThingGetNotFoundError"})

    assert api_surface.breaking_changes(api_surface.diff(before, after)) == [
        (
            "- `demo`: `GET /thing` raises `ThingGetError`, not `GetThingError`",
            "GetThingError",
        )
    ]


def test_a_removed_status_class_is_breaking_and_a_new_one_is_not():
    with_404 = _raising("GetThingError", **{"404": "GetThingNotFoundError"})
    without = _raising("GetThingError")

    removed = api_surface.breaking_changes(api_surface.diff(with_404, without))
    added = api_surface.breaking_changes(api_surface.diff(without, with_404))

    assert removed == [
        (
            "- `demo`: error class removed, `GetThingNotFoundError`",
            "GetThingNotFoundError",
        )
    ]
    assert added == []
    assert "error class added, `GetThingNotFoundError`" in _render(without, with_404)


def test_a_record_without_error_classes_compares_as_unchanged():
    """Records written before schema_version 7 carry no error classes."""
    before = _surface({"demo": _service(["GET /thing"])})

    assert api_surface.is_empty(api_surface.diff(before, _raising("GetThingError")))


def test_write_then_read_round_trips(tmp_path: Path):
    surface = _surface({"device": _service(["GET /device"])})
    path = tmp_path / "api_surface.json"

    api_surface.write(surface, path)

    assert api_surface.read(path) == surface


def test_summary_covers_mounted_and_types_only_services():
    """Rendered when no tagged release carries a surface record yet."""
    surface = _surface(
        {
            "device": _service(["GET /device", "POST /device"], ["Device"]),
            "kptr": _service([], ["PtrResult"], mounted=False),
            "plan": _service(["GET /plan"], []),
        },
        requirements={"protobuf": "protobuf>=7.35.1,<8"},
    )

    markdown = api_surface.render_summary(surface)

    assert "3 services (2 mounted on the client)" in markdown
    assert "3 REST operations" in markdown
    assert "**device**: `client.device`, 2 operations" in markdown
    assert "**plan**: `client.plan`, 1 operation" in markdown  # singular
    assert "**kptr**: types only, not mounted on the client" in markdown
    assert "`protobuf>=7.35.1,<8`" in markdown


def test_single_new_model_is_singular():
    before = _surface({"kptr": _service([], [])})
    after = _surface({"kptr": _service([], ["ListResolvedAddressesResponse"])})

    markdown = api_surface.render_markdown(
        api_surface.diff(before, after), since="v1.0.7"
    )

    assert "1 new model: `ListResolvedAddressesResponse`" in markdown


def test_renamed_field_is_flagged_breaking():
    """kmeta renamed ServiceNowConfig.credentialVaultId to credentialVaultName."""
    before = _surface({"kmeta": _service(fields={"Config": {"vaultId": _field()}})})
    after = _surface({"kmeta": _service(fields={"Config": {"vaultName": _field()}})})

    markdown = _render(before, after)

    assert markdown.startswith("### Breaking changes")
    assert "`kmeta`: field removed, `Config.vaultId`" in markdown
    assert "field added, `Config.vaultName` (`Optional[str]`)" in markdown


def test_new_optional_field_is_not_breaking_but_a_required_one_is():
    before = _surface({"demo": _service(fields={"Thing": {}})})
    optional = _surface({"demo": _service(fields={"Thing": {"note": _field()}})})
    required = _surface(
        {"demo": _service(fields={"Thing": {"name": _field("str", required=True)}})}
    )

    assert "Breaking changes" not in _render(before, optional)
    assert "new required field `Thing.name`" in _render(before, required)


def test_retyped_or_newly_required_field_is_breaking_but_relaxing_is_not():
    def surface(field: dict) -> dict:
        return _surface({"demo": _service(fields={"Thing": {"count": field}})})

    optional_str = surface(_field())
    assert "changed from" in _render(optional_str, surface(_field("Optional[int]")))
    assert "changed from" in _render(optional_str, surface(_field(required=True)))
    relaxed = _render(surface(_field(required=True)), optional_str)
    assert "Breaking changes" not in relaxed
    assert "`Thing.count`: `Optional[str]`, required to `Optional[str]`" in relaxed


def test_removed_enum_value_is_breaking_and_an_added_one_is_not():
    before = _surface({"demo": _service(enums={"Color": ["RED", "BLUE"]})})
    after = _surface({"demo": _service(enums={"Color": ["RED", "GREEN"]})})

    markdown = _render(before, after)

    assert "`demo`: enum value removed, `Color.BLUE`" in markdown
    assert "enum value added, `Color.GREEN`" in markdown
    names = [
        n for _, n in api_surface.breaking_changes(api_surface.diff(before, after))
    ]
    assert names == ["Color.BLUE"]


def test_operation_status_and_required_params_changes_are_reported():
    before = _surface({"demo": _service(["GET /thing"])})
    after = _surface({"demo": _service(["GET /thing"])})
    after["services"]["demo"]["operations"]["GET /thing"].update(
        status=201, required_params=["id"]
    )

    markdown = _render(before, after)

    assert "`GET /thing` succeeds with 201, not 200" in markdown
    assert "`demo`: `GET /thing` now requires `id`" in markdown


def test_a_record_without_fields_compares_as_unchanged():
    """Records written before schema_version 2 carry no fields or enums."""
    before = _surface({"demo": _service(models=["Thing"])})
    del before["services"]["demo"]["fields"], before["services"]["demo"]["enums"]
    after = _surface(
        {"demo": _service(models=["Thing"], fields={"Thing": {"note": _field()}})}
    )

    assert api_surface.is_empty(api_surface.diff(before, after))


def test_renamed_client_method_is_flagged_breaking():
    before = _surface({"alerting": _service(["GET /auto-acks"])})
    after = _surface({"alerting": _service(["GET /auto-acks"])})
    before["services"]["alerting"]["operations"]["GET /auto-acks"]["method"] = "list"
    after["services"]["alerting"]["operations"]["GET /auto-acks"]["method"] = (
        "alert_auto_ack_list"
    )

    delta = api_surface.diff(before, after)

    assert api_surface.breaking_changes(delta) == [
        (
            (
                "- `alerting`: `GET /auto-acks` is now "
                "`client.alerting.alert_auto_ack_list`, not `list`"
            ),
            "list",
        )
    ]
    assert "`list` to `alert_auto_ack_list`" in _render(before, after)


def test_a_record_without_method_names_compares_as_unchanged():
    """Records written before schema_version 4 carry no client method names."""
    before = _surface({"demo": _service(["GET /thing"])})
    after = _surface({"demo": _service(["GET /thing"])})
    after["services"]["demo"]["operations"]["GET /thing"]["method"] = "get_thing"

    assert api_surface.is_empty(api_surface.diff(before, after))


def test_breaking_changes_name_what_a_changelog_entry_must_mention():
    before = _surface(
        {"demo": _service(["GET /thing"], ["Old"], fields={"T": {"a": _field()}})}
    )
    after = _surface({"demo": _service([], [], fields={"T": {}})})

    names = [
        name
        for _, name in api_surface.breaking_changes(api_surface.diff(before, after))
    ]

    assert names == ["/thing", "Old", "T.a"]


def test_regeneration_alert_lists_changes_and_next_steps():
    before = _surface({"kmeta": _service(fields={"Config": {"vaultId": _field()}})})
    after = _surface({"kmeta": _service(fields={"Config": {"vaultName": _field()}})})

    alert = api_surface.render_regeneration_alert(before, after)

    assert "API SURFACE CHANGED since HEAD: 1 BREAKING change" in alert
    assert "`kmeta`: field removed, `Config.vaultId`" in alert
    assert "uv run poe check-changelog --since HEAD" in alert
    assert "uv run poe release-notes --since HEAD" in alert


def test_regeneration_alert_is_quiet_when_nothing_changed():
    surface = _surface({"demo": _service(["GET /thing"])})

    alert = api_surface.render_regeneration_alert(surface, surface)

    assert "unchanged since HEAD" in alert
    assert "CHANGED" not in alert


def test_regeneration_alert_says_when_there_is_no_committed_record():
    alert = api_surface.render_regeneration_alert(None, _surface({}))

    assert "No api_surface.json is committed at HEAD" in alert
