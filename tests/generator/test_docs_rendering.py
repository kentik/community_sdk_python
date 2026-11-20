# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Unit tests for docs_rendering._GROUP_CONFIG and _module_group consistency."""

from pathlib import Path

from scripts.generation.docs_rendering import (
    _GROUP_CONFIG,
    _LAYER_NAMES,
    _module_group,
)

_PACKAGE_ROOT = Path(__file__).resolve().parents[2] / "src" / "kentik_api"

_HAND_WRITTEN_DIRS = ("auth", "core", "errors", "transports")


def _hand_written_modules() -> list[str]:
    modules = ["kentik_api.client", "kentik_api.client_mixin"]
    for rel in _HAND_WRITTEN_DIRS:
        for py_file in sorted((_PACKAGE_ROOT / rel).rglob("*.py")):
            if py_file.name == "__init__.py" and py_file.parent.name != "errors":
                continue
            parts = py_file.relative_to(_PACKAGE_ROOT).with_suffix("").parts
            modules.append("kentik_api." + ".".join(parts).removesuffix(".__init__"))
    return modules


def test_every_hand_written_module_maps_to_a_group():
    """No hand-written module may map to None, or it silently vanishes from the diagram."""
    unmapped = [m for m in _hand_written_modules() if _module_group(m) is None]
    assert not unmapped, (
        f"_module_group() returned None for {unmapped}; these modules would be "
        f"silently omitted from the generated architecture diagram. Add a branch "
        f"in _module_group() and a label in _GROUP_CONFIG."
    )


def test_every_layer_in_group_config_has_a_layer_name():
    """Every layer key referenced in _GROUP_CONFIG must have an entry in _LAYER_NAMES."""
    missing = {
        layer for layer, _ in _GROUP_CONFIG.values() if layer not in _LAYER_NAMES
    }
    assert not missing, (
        f"Layer keys in _GROUP_CONFIG with no _LAYER_NAMES entry: {missing}"
    )


def test_group_config_covers_all_module_group_return_values():
    """_module_group() should only return labels that appear in _GROUP_CONFIG."""
    sample_modules = [
        ("kentik_api.client", None),
        ("kentik_api.client_mixin", None),
        ("kentik_api.auth.credentials", None),
        ("kentik_api.core.api_config", None),
        ("kentik_api.core.rest_runtime", None),
        ("kentik_api.core.grpc_runtime", None),
        ("kentik_api.errors", None),
        ("kentik_api.transports.base", None),
        ("kentik_api.transports.rest_client", None),
        ("kentik_api.transports.grpc_client", None),
        ("kentik_api.gen.device.error", None),
        ("kentik_api.gen.device.models.Device", None),
        ("kentik_api.gen.device.pb.device_pb2", None),
    ]
    for module_name, source_file in sample_modules:
        label = _module_group(module_name, source_file)
        if label is not None:
            assert label in _GROUP_CONFIG, (
                f"_module_group({module_name!r}) returned {label!r} "
                f"which is not in _GROUP_CONFIG"
            )


def test_group_config_has_no_duplicate_layer_assignments():
    """Sanity check: each group label appears exactly once in _GROUP_CONFIG."""
    assert len(_GROUP_CONFIG) == len(set(_GROUP_CONFIG)), (
        "Duplicate keys in _GROUP_CONFIG"
    )


import json  # noqa: E402
import re  # noqa: E402

import pytest  # noqa: E402

from scripts.generation import docs_rendering  # noqa: E402

_REPO = Path(__file__).resolve().parents[2]
_MARKER_BLOCK = re.compile(
    r"(<!-- kentik-gen:([\w-]+) -->).*?(<!-- /kentik-gen:\2 -->)", re.DOTALL
)
_GUIDES = ("quickstart", "rest", "grpc", "generation")


def _without_marker_contents(text: str) -> str:
    return _MARKER_BLOCK.sub(r"\1\3", text)


def _marker(text: str, name: str) -> str:
    match = re.search(
        rf"<!-- kentik-gen:{name} -->(.*?)<!-- /kentik-gen:{name} -->", text, re.DOTALL
    )
    assert match, name
    return match.group(1)


@pytest.mark.parametrize(
    "rel",
    [
        "src/kentik_api/gen/README.md",
        "src/kentik_api/gen/device/README.md",
        "src/kentik_api/gen/alerting/README.md",
        "src/kentik_api/gen/core/README.md",
    ],
)
def test_readmes_reproduce_the_committed_ones_exactly(sandbox, rel):
    docs_rendering.generate()

    assert (sandbox.root / rel).read_text() == (_REPO / rel).read_text()


def test_architecture_page_matches_committed_apart_from_edge_counts(sandbox):
    docs_rendering.generate()

    rel = "docs/sphinx/sdk_runtime_architecture.md"
    service_dependent = [
        (re.compile(r'\|"\d+ imports?"\|'), "|n|"),
        (re.compile(r" \(\d+\)"), " (n)"),
        (re.compile(r"\d+ import statements"), "n import statements"),
        (re.compile(r"\d+ services, \d+ operations"), "n services, n operations"),
        (re.compile(r"\d+ Services are in that state today: [^\n]*"), "N Services ..."),
        (re.compile(r"\n## REST-Only Services\n.*\Z", re.DOTALL), ""),
    ]

    def normalized(text: str) -> str:
        for pattern, replacement in service_dependent:
            text = pattern.sub(replacement, text)
        return text

    produced = (sandbox.root / rel).read_text()
    assert normalized(produced) == normalized((_REPO / rel).read_text())
    assert '|"51 imports"|' not in produced
    assert "1 Services are in that state today: `core`." in produced


def test_architecture_page_lists_every_layer(sandbox):
    docs_rendering.generate()

    page = (sandbox.docs / "sdk_runtime_architecture.md").read_text()
    for layer in docs_rendering._LAYER_NAMES.values():
        assert layer in page


def test_architecture_table_shows_wrappers_using_models_and_proto_stubs(sandbox):
    docs_rendering.generate()

    page = (sandbox.docs / "sdk_runtime_architecture.md").read_text()
    row = next(
        line
        for line in page.splitlines()
        if line.startswith("| Generated Service Wrappers |")
    )
    assert "Generated Models (" in row
    assert "Generated Proto Stubs (" in row


def test_dependency_explorer_draws_only_real_imports(sandbox):
    docs_rendering.generate()

    page = (sandbox.docs / "sdk_runtime_architecture.md").read_text()
    blobs = re.findall(
        r'<script type="application/json" id="diagram-data">(.*?)</script>', page
    )
    assert len(blobs) == 2
    data = json.loads(blobs[1])["deps-svg"]
    assert set(data["parts"]) == set(docs_rendering._PARTS)
    assert all("import statements" in label for label in data["links"].values())
    assert (sandbox.docs / "_static" / "explorer.js").exists()


def test_dependency_explorer_fails_on_a_wire_with_no_import():
    with pytest.raises(ValueError, match="draws imports that do not exist"):
        docs_rendering._dependency_explorer({})


@pytest.mark.parametrize("guide", _GUIDES)
def test_guide_prose_outside_marker_blocks_is_left_untouched(sandbox, guide):
    rel = f"docs/sphinx/guides/{guide}.md"

    docs_rendering.generate()

    produced = (sandbox.root / rel).read_text()
    assert _without_marker_contents(produced) == _without_marker_contents(
        (_REPO / rel).read_text()
    )


def test_marker_blocks_describe_the_services_actually_present(sandbox):
    docs_rendering.generate()

    guides = sandbox.docs / "guides"
    assert _marker((guides / "generation.md").read_text(), "service-count") == "3"
    assert _marker((sandbox.docs / "README.md").read_text(), "service-count") == "3"
    quickstart = (guides / "quickstart.md").read_text()
    assert "client.device.list()" in _marker(quickstart, "first-call-example")
    assert "as_group" not in quickstart
    grpc_md = (guides / "grpc.md").read_text()
    assert "ListDevices" in _marker(grpc_md, "grpc-callflow-diagram")


def test_generate_is_idempotent(sandbox):
    docs_rendering.generate()
    first = {p: p.read_text() for p in sandbox.root.rglob("*.md")}

    docs_rendering.generate()

    assert {p: p.read_text() for p in sandbox.root.rglob("*.md")} == first


def test_services_without_a_wrapper_are_named(sandbox):
    section = "\n".join(docs_rendering._services_without_wrappers_section())

    assert "`core`" in section
    assert "`device`" not in section


def test_no_section_when_every_service_has_a_wrapper(sandbox):
    import shutil

    shutil.rmtree(sandbox.gen / "core")

    assert docs_rendering._services_without_wrappers_section() == []


def test_rest_only_services_are_marked_with_their_local_schema_source(sandbox):
    docs_rendering.generate(frozenset({"device"}))

    page = (sandbox.docs / "sdk_runtime_architecture.md").read_text()
    section = page.split("## REST-Only Services", 1)[1]
    assert "`schema/openapi/`" in section
    assert "`device`" in section
    assert "`alerting`" not in section
    readme = (sandbox.gen / "device" / "README.md").read_text()
    assert "local schema base, `schema/openapi/`. It is REST only." in readme
    other = (sandbox.gen / "alerting" / "README.md").read_text()
    assert "the Kentik OpenAPI v3 schema." in other


def test_no_rest_only_section_without_local_services(sandbox):
    docs_rendering.generate()

    page = (sandbox.docs / "sdk_runtime_architecture.md").read_text()
    assert "REST-Only Services" not in page


def test_replace_marker_rewrites_only_the_named_block():
    text = "a <!-- kentik-gen:x -->old<!-- /kentik-gen:x --> b <!-- kentik-gen:y -->keep<!-- /kentik-gen:y -->"

    result = docs_rendering._replace_marker(text, "x", "new")

    assert (
        result
        == "a <!-- kentik-gen:x -->new<!-- /kentik-gen:x --> b <!-- kentik-gen:y -->keep<!-- /kentik-gen:y -->"
    )


def test_guide_update_skips_when_no_generated_tree_exists(sandbox):
    import shutil

    before = (sandbox.docs / "guides" / "quickstart.md").read_text()
    shutil.rmtree(sandbox.gen)

    docs_rendering._update_guide_snippets()

    assert (sandbox.docs / "guides" / "quickstart.md").read_text() == before


@pytest.mark.parametrize(
    ("current", "level", "module", "expected"),
    [
        (
            "kentik_api.gen.device.services.device",
            1,
            "DeviceService",
            "kentik_api.gen.device.services.DeviceService",
        ),
        (
            "kentik_api.gen.device.services.device",
            2,
            "models",
            "kentik_api.gen.device.models",
        ),
        ("kentik_api.core.rest_runtime", 0, "httpx", "httpx"),
    ],
)
def test_resolve_import_from(current, level, module, expected):
    assert docs_rendering._resolve_import_from(current, level, module) == expected


def test_grpc_stub_method_name_reads_the_wrapper():
    wrapper = _REPO / "src" / "kentik_api" / "gen" / "device" / "services" / "device.py"

    assert docs_rendering._grpc_stub_method_name(wrapper, "list") == "ListDevices"
    assert docs_rendering._grpc_stub_method_name(wrapper, "no_such_method") is None
