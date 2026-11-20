# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from scripts.generation._shared import INTERNAL_GEN_DIRS, iter_service_dirs
from scripts.generation.parity import (
    drop_superseded_swagger_files,
    merge_local_schema_base,
    select_latest_swagger_files_by_service,
    validate_generated_service_parity,
    validate_schema_files,
    validate_schema_files_or_raise,
    validate_selected_services_or_raise,
)


def _write_swagger(base: Path, service: str, version: str, filename: str) -> Path:
    swagger_dir = base / service / version
    swagger_dir.mkdir(parents=True, exist_ok=True)
    swagger_path = swagger_dir / filename
    swagger_path.write_text("{}", encoding="utf-8")
    return swagger_path


def _valid_schema_file(tmp_path: Path, name: str) -> Path:
    path = tmp_path / name
    path.write_text(
        json.dumps({"swagger": "2.0", "info": {"title": "t"}, "paths": {}}),
        encoding="utf-8",
    )
    return path


def _function_by_name(source: str, name: str) -> ast.FunctionDef | None:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return node
    return None


def _handler_contains_text(handler: ast.ExceptHandler, text: str) -> bool:
    return any(
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and text in node.value
        for node in ast.walk(handler)
    )


def test_select_latest_swagger_files_by_service_picks_newest_version(tmp_path: Path):
    _write_swagger(tmp_path, "device", "v202211", "device.swagger.json")
    _write_swagger(tmp_path, "device", "v202309", "device.swagger.json")
    _write_swagger(tmp_path, "user", "v202211", "user.swagger.json")

    by_service, selected_count, ignored_count = select_latest_swagger_files_by_service(
        tmp_path
    )

    assert set(by_service) == {"device", "user"}
    assert len(by_service["device"]) == 1
    assert by_service["device"][0]["version"] == "v202309"
    assert selected_count == 2
    assert ignored_count == 1


def test_select_latest_swagger_files_by_service_groups_multiple_files_per_service(
    tmp_path: Path,
):
    _write_swagger(tmp_path, "alerting", "v1", "alerting.swagger.json")
    _write_swagger(tmp_path, "alerting", "v1", "alerting_message.swagger.json")

    by_service, selected_count, ignored_count = select_latest_swagger_files_by_service(
        tmp_path
    )

    assert len(by_service["alerting"]) == 2
    assert selected_count == 2
    assert ignored_count == 0


def _tagged_swagger(
    base: Path, service: str, version: str, filename: str, *tags: str
) -> None:
    path = _write_swagger(base, service, version, filename)
    paths = {f"/{tag}/{i}": {"get": {"tags": [tag]}} for i, tag in enumerate(tags)}
    path.write_text(json.dumps({"paths": paths}), encoding="utf-8")


def _drop(base: Path) -> tuple[dict[str, list[str]], list[str]]:
    selected, _, _ = select_latest_swagger_files_by_service(base)
    kept, dropped = drop_superseded_swagger_files(selected)
    return (
        {s: [f["filename"] for f in files] for s, files in kept.items()},
        [f["filename"] for f in dropped],
    )


def test_renamed_file_drops_the_old_version_whichever_name_sorts_last(
    tmp_path: Path,
):
    # The old name sorts last, so without the drop it would be generated last and win.
    _tagged_swagger(tmp_path, "foo", "v202401beta1", "z_foo.swagger.json", "FooService")
    _tagged_swagger(tmp_path, "foo", "v202501", "a_foo.swagger.json", "FooService")

    assert _drop(tmp_path) == ({"foo": ["a_foo.swagger.json"]}, ["z_foo.swagger.json"])


def test_files_with_distinct_modules_and_no_operations_are_kept(tmp_path: Path):
    _tagged_swagger(tmp_path, "alerting", "v202303", "alert.swagger.json", "Alerts")
    _tagged_swagger(tmp_path, "alerting", "v202505", "mitig.swagger.json", "Mitig")
    _tagged_swagger(tmp_path, "alerting", "v202101", "types.swagger.json")

    kept, dropped = _drop(tmp_path)

    assert len(kept["alerting"]) == 3
    assert dropped == []


@pytest.mark.parametrize(
    ("old_tags", "new_version"),
    [
        (("FooService", "BarService"), "v202501"),  # old file not fully replaced
        (("FooService",), "v202401beta1"),  # same version, no newer file
    ],
)
def test_shared_module_without_a_full_replacement_fails(
    tmp_path: Path, old_tags: tuple[str, ...], new_version: str
):
    _tagged_swagger(tmp_path, "foo", "v202401beta1", "old.swagger.json", *old_tags)
    _tagged_swagger(tmp_path, "foo", new_version, "new.swagger.json", "FooService")

    with pytest.raises(RuntimeError, match="both write REST module `FooService`"):
        _drop(tmp_path)


def test_validate_generated_service_parity_passes_when_sets_match(tmp_path: Path):
    (tmp_path / "device").mkdir()
    (tmp_path / "user").mkdir()

    validate_generated_service_parity({"device", "user"}, tmp_path)


def test_validate_generated_service_parity_raises_on_missing_service(tmp_path: Path):
    (tmp_path / "device").mkdir()

    with pytest.raises(RuntimeError, match="do not match"):
        validate_generated_service_parity({"device", "user"}, tmp_path)


def test_validate_generated_service_parity_raises_on_extra_directory(tmp_path: Path):
    (tmp_path / "device").mkdir()
    (tmp_path / "leftover").mkdir()

    with pytest.raises(RuntimeError, match="do not match"):
        validate_generated_service_parity({"device"}, tmp_path)


def test_validate_schema_files_passes_valid_files(tmp_path: Path):
    files = [
        _valid_schema_file(tmp_path, "device.swagger.json"),
        _valid_schema_file(tmp_path, "user.swagger.json"),
    ]

    assert validate_schema_files(files) == []


def test_validate_schema_files_rejects_empty_file(tmp_path: Path):
    empty = tmp_path / "empty.swagger.json"
    empty.write_text("", encoding="utf-8")

    failures = validate_schema_files([empty])

    assert len(failures) == 1
    assert failures[0]["path"] == empty
    assert "empty" in failures[0]["reason"]


def test_validate_schema_files_rejects_invalid_json(tmp_path: Path):
    broken = tmp_path / "broken.swagger.json"
    broken.write_text("{not json", encoding="utf-8")

    failures = validate_schema_files([broken])

    assert len(failures) == 1
    assert "invalid JSON" in failures[0]["reason"]


def test_validate_schema_files_rejects_missing_required_keys(tmp_path: Path):
    incomplete = tmp_path / "incomplete.swagger.json"
    incomplete.write_text(json.dumps({"info": {"title": "t"}}), encoding="utf-8")

    failures = validate_schema_files([incomplete])

    assert len(failures) == 1
    assert "paths" in failures[0]["reason"]
    assert "swagger/openapi" in failures[0]["reason"]


def test_validate_schema_files_reports_all_failures_before_raising(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    empty = tmp_path / "empty.swagger.json"
    empty.write_text("", encoding="utf-8")
    broken = tmp_path / "broken.swagger.json"
    broken.write_text("{not json", encoding="utf-8")
    valid = _valid_schema_file(tmp_path, "device.swagger.json")

    failures = validate_schema_files([empty, broken, valid])
    assert {f["path"] for f in failures} == {empty, broken}

    with pytest.raises(RuntimeError, match="structural validation"):
        validate_schema_files_or_raise([empty, broken, valid])

    printed = capsys.readouterr().out
    assert str(empty) in printed
    assert str(broken) in printed
    assert str(valid) not in printed


def test_validate_schema_files_or_raise_rejects_empty_selection():
    with pytest.raises(RuntimeError, match="No swagger files selected"):
        validate_schema_files_or_raise([])


def test_a_service_whose_swagger_files_were_renamed_away_fails_before_the_wipe(
    tmp_path: Path,
):
    _write_swagger(tmp_path, "device", "v202308", "device.swagger.json")
    (tmp_path / "user" / "v202211").mkdir(parents=True)
    (tmp_path / "user" / "v202211" / "user.openapi.json").write_text("{}")
    selected, _, _ = select_latest_swagger_files_by_service(tmp_path)

    with pytest.raises(RuntimeError, match="without a swagger file: user"):
        validate_selected_services_or_raise({"device", "user"}, set(selected))


def test_every_service_with_a_swagger_file_passes_the_pre_wipe_check():
    validate_selected_services_or_raise({"device"}, {"device"})


def test_local_schema_base_services_join_upstream_and_pass_parity(tmp_path: Path):
    upstream_base, local_base = tmp_path / "upstream", tmp_path / "local"
    _write_swagger(upstream_base, "device", "v202308", "device.swagger.json")
    _write_swagger(local_base, "v5", "v5", "v5.swagger.json")
    upstream, _, _ = select_latest_swagger_files_by_service(upstream_base)
    local, _, _ = select_latest_swagger_files_by_service(local_base)

    merged = merge_local_schema_base(upstream, local)

    assert set(merged) == {"device", "v5"}
    assert merged["v5"][0]["version"] == "v5"
    generated = tmp_path / "gen"
    for service in merged:
        (generated / service).mkdir(parents=True)
    validate_generated_service_parity(set(merged), generated)


def test_a_service_in_both_schema_bases_fails(tmp_path: Path):
    upstream_base, local_base = tmp_path / "upstream", tmp_path / "local"
    _write_swagger(upstream_base, "v5", "v202701", "v5.swagger.json")
    _write_swagger(local_base, "v5", "v5", "v5.swagger.json")
    upstream, _, _ = select_latest_swagger_files_by_service(upstream_base)
    local, _, _ = select_latest_swagger_files_by_service(local_base)

    with pytest.raises(RuntimeError, match="both the upstream schema.*: v5"):
        merge_local_schema_base(upstream, local)


def test_a_broken_local_schema_file_fails_validation(tmp_path: Path):
    broken = tmp_path / "v5" / "v5" / "v5.swagger.json"
    broken.parent.mkdir(parents=True)
    broken.write_text('{"openapi": "3.0.0", "info": {}', encoding="utf-8")

    with pytest.raises(RuntimeError, match="failed structural validation"):
        validate_schema_files_or_raise([broken])


def test_the_protoc_failure_handler_reraises():
    source = (
        Path(__file__).resolve().parents[2] / "scripts" / "generate_sdk.py"
    ).read_text(encoding="utf-8")
    func = _function_by_name(source, "_compile_service_protos")
    assert func is not None

    handlers = [
        node
        for node in ast.walk(func)
        if isinstance(node, ast.ExceptHandler)
        and node.type is not None
        and "CalledProcessError" in ast.unparse(node.type)
    ]
    assert handlers

    protoc_handler = next(
        (
            handler
            for handler in handlers
            if _handler_contains_text(handler, "Protobuf generation failed")
        ),
        None,
    )
    assert protoc_handler is not None
    assert any(isinstance(node, ast.Raise) for node in ast.walk(protoc_handler)), (
        "protoc failures must fail generation, not only print logs"
    )


def test_validate_schema_files_catches_truncated_file_like_2026_08_26_incident(
    tmp_path: Path,
):
    truncated = tmp_path / "device.swagger.json"
    truncated.write_text('  "swagger": "2.0",', encoding="utf-8")

    failures = validate_schema_files([truncated])

    assert len(failures) == 1
    assert "invalid JSON" in failures[0]["reason"]


def _make_gen_tree(root: Path, names: list[str]) -> None:
    """Builds a gen/-shaped tree: each name a directory holding models/."""
    for name in names:
        (root / name / "models").mkdir(parents=True, exist_ok=True)


def test_iter_service_dirs_excludes_every_internal_dir(tmp_path: Path):
    _make_gen_tree(tmp_path, ["device", "alerting", *INTERNAL_GEN_DIRS])

    names = [d.name for d in iter_service_dirs(tmp_path)]

    assert names == ["alerting", "device"], "sorted, internal dirs excluded"
    for internal in INTERNAL_GEN_DIRS:
        assert internal not in names


def test_iter_service_dirs_includes_operationless_service(tmp_path: Path):
    _make_gen_tree(tmp_path, ["device"])
    (tmp_path / "operationless" / "models").mkdir(parents=True)
    (tmp_path / "operationless" / "services").mkdir()
    (tmp_path / "operationless" / "services" / "__init__.py").write_text("")

    names = [d.name for d in iter_service_dirs(tmp_path)]

    assert names == ["device", "operationless"]


def test_iter_service_dirs_skips_files_and_returns_sorted(tmp_path: Path):
    _make_gen_tree(tmp_path, ["zeta", "alpha"])
    (tmp_path / "README.md").write_text("not a service", encoding="utf-8")

    names = [d.name for d in iter_service_dirs(tmp_path)]

    assert names == ["alpha", "zeta"]


def test_iter_service_dirs_regression_pb_companions_excluded_core_included(
    tmp_path: Path,
):
    _make_gen_tree(tmp_path, ["core", "device", "pb_companions"])

    names = [d.name for d in iter_service_dirs(tmp_path)]

    assert "core" in names, "core is a real Service and must not be excluded"
    assert "pb_companions" not in names, "pb_companions is generator-internal"
    assert len(names) == 2
