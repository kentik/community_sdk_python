# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Tests for scripts/generate_sdk.py top-level helpers.

All tests use tmp_path so no schema download or full generation run is needed
for the unit tests. The integration test
(test_the_real_alert_schema_keeps_acknowledgement_an_object) also skips
gracefully when the local schema repo is absent.
"""

from __future__ import annotations

import ast
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# generate_sdk.py uses `from generation import ...` (script-style absolute
# import that requires scripts/ on sys.path). Add scripts/ so the import
# resolves the same way it does when the script runs directly.
_scripts_dir = Path(__file__).resolve().parents[2] / "scripts"
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from generate_sdk import (  # noqa: E402  # type: ignore[import-not-found]
    GENERATED_DOC_PAGES,
    PROJECT_ROOT,
    _fix_module_level_classvar,
    _pb_stem,
    _proto_collisions,
    _qualify_colliding_imports,
    _relink_pb2_dependency_imports,
    _rewrite_grpc_imports,
    _silence_grpc_experimental,
    check_model_names,
    clean_schema_names,
    fetch_schema,
    get_schema_root,
    hoist_inline_request_bodies,
    inline_request_body_refs,
    local_schema_commit,
    oneof_members_by_definition,
    openapi_generator_cmd,
    patched_swagger,
    read_schema_pin,
    relax_oneof_required,
    relax_response_message_required,
    rename_models,
    restored_on_failure,
    schema_model_names,
)
from google.protobuf import descriptor_pb2  # noqa: E402


def test_generator_runs_from_the_locked_environment_by_default(monkeypatch):
    monkeypatch.delenv("OPENAPI_GENERATOR_FROM", raising=False)
    monkeypatch.delenv("OPENAPI_GENERATOR_CMD", raising=False)

    cmd = openapi_generator_cmd(Path("in.json"), Path("out"))

    assert cmd[:4] == [sys.executable, "-m", "openapi_python_generator", "in.json"]


def test_a_fork_source_runs_through_uvx(monkeypatch):
    monkeypatch.setenv("OPENAPI_GENERATOR_FROM", "git+https://example.invalid/fork.git")
    monkeypatch.delenv("OPENAPI_GENERATOR_CMD", raising=False)

    cmd = openapi_generator_cmd(Path("in.json"), Path("out"))

    assert cmd[:5] == [
        "uvx",
        "--from",
        "git+https://example.invalid/fork.git",
        "openapi-python-generator",
        "in.json",
    ]


def test_rewrite_bare_import():
    result = _rewrite_grpc_imports("import device_pb2\n")
    assert result == "from . import device_pb2\n"


def test_rewrite_parenthesised_from_import():
    result = _rewrite_grpc_imports(
        "from kentik.device.v202308 import (\n    device_pb2 as _device,\n)\n"
    )
    assert "from . import device_pb2 as _device" in result


def test_rewrite_unparenthesised_from_import():
    result = _rewrite_grpc_imports(
        "from kentik.device.v202308 import device_pb2 as _device\n"
    )
    assert result == "from . import device_pb2 as _device\n"


def test_rewrite_leaves_non_pb2_imports_unchanged():
    content = "from kentik_api.core.api_config import APIConfig\n"
    assert _rewrite_grpc_imports(content) == content


def test_grpc_directive_is_added_once():
    once = _silence_grpc_experimental("import grpc\n")

    assert once.startswith("# pyright: reportAttributeAccessIssue=false\n")
    assert _silence_grpc_experimental(once) == once


def test_module_level_classvar_becomes_int_and_class_body_keeps_it():
    stub = (
        "VISIBILITY_FIELD_NUMBER: _ClassVar[int]\n"
        "class Device(_message.Message):\n"
        "    ID_FIELD_NUMBER: _ClassVar[int]\n"
    )

    assert _fix_module_level_classvar(stub) == (
        "VISIBILITY_FIELD_NUMBER: int\n"
        "class Device(_message.Message):\n"
        "    ID_FIELD_NUMBER: _ClassVar[int]\n"
    )


_MINIMAL_SCHEMA_WITH_REF_BODY = {
    "paths": {
        "/things": {
            "post": {
                "operationId": "CreateThing",
                "requestBody": {"$ref": "#/components/requestBodies/Thing"},
                "responses": {"200": {}},
            }
        },
        "/things/{id}": {
            "put": {
                "operationId": "UpdateThing",
                "requestBody": {"$ref": "#/components/requestBodies/Thing"},
                "responses": {"200": {}},
            },
            "get": {
                "operationId": "GetThing",
                "responses": {"200": {}},
            },
        },
    },
    "components": {
        "requestBodies": {
            "Thing": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Thing"}
                    }
                },
                "required": True,
            }
        },
        "schemas": {
            "Thing": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
            }
        },
    },
}


def test_patch_schema_inlines_request_body_ref(tmp_path: Path):
    swagger_path = tmp_path / "things.swagger.json"
    original = json.dumps(_MINIMAL_SCHEMA_WITH_REF_BODY)
    swagger_path.write_text(original)

    with patched_swagger(swagger_path, version="v202411alpha1") as patched_path:
        result = json.loads(Path(patched_path).read_text())

    post_rb = result["paths"]["/things"]["post"]["requestBody"]
    put_rb = result["paths"]["/things/{id}"]["put"]["requestBody"]

    assert "$ref" not in post_rb, "POST requestBody $ref should be inlined"
    assert "content" in post_rb
    assert "application/json" in post_rb["content"]

    assert "$ref" not in put_rb, "PUT requestBody $ref should be inlined"
    assert "content" in put_rb

    assert swagger_path.read_text() == original, (
        "patched_swagger must not modify the schema checkout"
    )


def test_patch_schema_leaves_inline_request_body_unchanged(tmp_path: Path):
    inline_rb = {
        "content": {
            "application/json": {"schema": {"$ref": "#/components/schemas/Thing"}}
        },
        "required": True,
    }
    schema = {
        "paths": {
            "/things": {
                "post": {
                    "operationId": "CreateThing",
                    "requestBody": inline_rb,
                    "responses": {"200": {}},
                }
            }
        },
        "components": {"schemas": {"Thing": {"type": "object"}}},
    }
    swagger_path = tmp_path / "things.swagger.json"
    original = json.dumps(schema)
    swagger_path.write_text(original)

    with patched_swagger(swagger_path, version="v202411alpha1") as patched_path:
        result = json.loads(Path(patched_path).read_text())

    rb = result["paths"]["/things"]["post"]["requestBody"]
    assert "content" in rb
    assert "$ref" not in rb
    assert swagger_path.read_text() == original


def test_patch_schema_leaves_operations_without_request_body_unchanged(tmp_path: Path):
    schema = {
        "paths": {
            "/things/{id}": {
                "get": {"operationId": "GetThing", "responses": {"200": {}}},
                "delete": {
                    "operationId": "DeleteThing",
                    "responses": {"200": {}},
                },
            }
        },
        "components": {},
    }
    swagger_path = tmp_path / "things.swagger.json"
    original = json.dumps(schema)
    swagger_path.write_text(original)

    with patched_swagger(swagger_path, version="v202411alpha1") as patched_path:
        result = json.loads(Path(patched_path).read_text())

    assert "requestBody" not in result["paths"]["/things/{id}"]["get"]
    assert "requestBody" not in result["paths"]["/things/{id}"]["delete"]
    assert swagger_path.read_text() == original


def test_clean_schema_names_strips_version_prefix_from_definitions():
    schema = {
        "definitions": {
            "v202404beta1Thing": {"type": "object"},
        }
    }
    result = clean_schema_names(schema, "v202404beta1")
    assert "Thing" in result["definitions"]
    assert "v202404beta1Thing" not in result["definitions"]


def test_clean_schema_names_rewrites_refs():
    schema = {
        "paths": {
            "/thing": {
                "get": {
                    "responses": {
                        "200": {"schema": {"$ref": "#/definitions/v202404beta1Thing"}}
                    }
                }
            }
        },
        "definitions": {},
    }
    result = clean_schema_names(schema, "v202404beta1")
    ref = result["paths"]["/thing"]["get"]["responses"]["200"]["schema"]["$ref"]
    assert "v202404beta1" not in ref


def test_clean_schema_names_does_not_mutate_input():
    schema = {"definitions": {"v202404beta1Thing": {"type": "object"}}}
    original_keys = set(schema["definitions"].keys())
    clean_schema_names(schema, "v202404beta1")
    assert set(schema["definitions"].keys()) == original_keys


def test_inline_request_body_refs_resolves_ref():
    schema = {
        "paths": {
            "/things": {
                "post": {"requestBody": {"$ref": "#/components/requestBodies/Thing"}}
            }
        },
        "components": {
            "requestBodies": {
                "Thing": {"content": {"application/json": {}}, "required": True}
            }
        },
    }
    result = inline_request_body_refs(schema)
    rb = result["paths"]["/things"]["post"]["requestBody"]
    assert "content" in rb
    assert "$ref" not in rb


def test_inline_request_body_refs_does_not_mutate_input():
    schema = {
        "paths": {
            "/things": {
                "post": {"requestBody": {"$ref": "#/components/requestBodies/Thing"}}
            }
        },
        "components": {"requestBodies": {"Thing": {"content": {}}}},
    }
    post = schema["paths"]["/things"]["post"]
    inline_request_body_refs(schema)
    assert "$ref" in post["requestBody"]


def _inline_body_schema() -> dict:
    return {
        "paths": {
            "/capabilities/{capability.name}": {
                "patch": {
                    "operationId": "CapabilityAdminService_UpdateCapability",
                    "tags": ["CapabilityAdminService"],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "title": "capability",
                                    "properties": {"displayName": {"type": "string"}},
                                    "required": ["capability"],
                                }
                            }
                        }
                    },
                }
            }
        },
        "components": {"schemas": {}},
    }


def test_inline_request_body_is_hoisted_to_a_named_schema():
    schema = hoist_inline_request_bodies(_inline_body_schema())

    name = "CapabilityAdminServiceUpdateCapabilityBody"
    media = schema["paths"]["/capabilities/{capability.name}"]["patch"]["requestBody"]
    assert media["content"]["application/json"]["schema"] == {
        "$ref": f"#/components/schemas/{name}"
    }
    assert schema["components"]["schemas"][name] == {
        "type": "object",
        "properties": {"displayName": {"type": "string"}},
    }


def test_hoisting_refuses_to_overwrite_an_existing_schema():
    schema = _inline_body_schema()
    schema["components"]["schemas"]["CapabilityAdminServiceUpdateCapabilityBody"] = {}

    with pytest.raises(ValueError, match="exists"):
        hoist_inline_request_bodies(schema)


def test_patched_swagger_does_not_modify_original(tmp_path: Path):
    schema = {
        "paths": {},
        "components": {"schemas": {"v202404beta1Thing": {"type": "object"}}},
    }
    swagger_path = tmp_path / "things.swagger.json"
    swagger_path.write_text(json.dumps(schema), encoding="utf-8")
    original_text = swagger_path.read_text()

    with patched_swagger(swagger_path, "v202404beta1") as tmp_path_arg:
        patched = json.loads(Path(tmp_path_arg).read_text())
        assert "Thing" in patched["components"]["schemas"]

    assert swagger_path.read_text() == original_text
    assert not tmp_path_arg.exists()


def test_patched_swagger_gives_each_model_and_reference_its_public_name(
    tmp_path: Path,
):
    schema = {
        "paths": {},
        "components": {
            "schemas": {
                "labelv202210Label": {"type": "object"},
                "ListLabelsResponse": {
                    "properties": {
                        "labels": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/labelv202210Label"},
                        }
                    }
                },
            }
        },
    }
    swagger_path = tmp_path / "label.swagger.json"
    swagger_path.write_text(json.dumps(schema), encoding="utf-8")

    assert schema_model_names(swagger_path, "v202210") == [
        "labelv202210Label",
        "ListLabelsResponse",
    ]
    with patched_swagger(
        swagger_path, "v202210", model_renames={"labelv202210Label": "Label"}
    ) as patched_path:
        schemas = json.loads(patched_path.read_text())["components"]["schemas"]

    assert list(schemas) == ["Label", "ListLabelsResponse"]
    items = schemas["ListLabelsResponse"]["properties"]["labels"]["items"]
    assert items == {"$ref": "#/components/schemas/Label"}


def test_rename_models_can_swap_two_names():
    schema = {
        "components": {"schemas": {"A": {"$ref": "#/components/schemas/B"}, "B": {}}}
    }
    result = rename_models(schema, {"A": "B", "B": "A"})
    assert result["components"]["schemas"] == {
        "B": {"$ref": "#/components/schemas/A"},
        "A": {},
    }
    assert schema["components"]["schemas"]["A"] == {"$ref": "#/components/schemas/B"}


def _descriptor_set() -> descriptor_pb2.FileDescriptorSet:
    message = descriptor_pb2.DescriptorProto(name="ExternalContext")
    message.oneof_decl.add(name="context")
    message.oneof_decl.add(name="_note")
    message.field.add(name="servicenow", json_name="servicenow", oneof_index=0)
    message.field.add(name="jira_cloud", json_name="jiraCloud", oneof_index=0)
    message.field.add(name="id", json_name="id")
    message.field.add(
        name="note", json_name="note", oneof_index=1, proto3_optional=True
    )
    nested = message.nested_type.add(name="Inner")
    nested.oneof_decl.add(name="kind")
    nested.field.add(name="a", json_name="a", oneof_index=0)
    file = descriptor_pb2.FileDescriptorProto(package="kentik.alerting.v202505")
    file.message_type.append(message)
    return descriptor_pb2.FileDescriptorSet(file=[file])


def test_oneof_members_by_definition_uses_swagger_names_and_skips_optional():
    assert oneof_members_by_definition(_descriptor_set()) == {
        "v202505ExternalContext": {"servicenow", "jiraCloud"},
        "v202505ExternalContextInner": {"a"},
    }


def test_patched_swagger_drops_oneof_members_from_required(tmp_path: Path):
    schema = {
        "components": {
            "schemas": {
                "v202505ExternalContext": {
                    "type": "object",
                    "required": ["servicenow", "jiraCloud", "id"],
                },
                "v202505ExternalContextInner": {"required": ["a"]},
            }
        }
    }
    swagger_path = tmp_path / "alert.swagger.json"
    swagger_path.write_text(json.dumps(schema), encoding="utf-8")
    members = oneof_members_by_definition(_descriptor_set())

    with patched_swagger(swagger_path, "v202505", members) as patched_path:
        schemas = json.loads(patched_path.read_text())["components"]["schemas"]

    assert schemas["ExternalContext"]["required"] == ["id"]
    assert "required" not in schemas["ExternalContextInner"]


def test_relax_oneof_required_does_not_mutate_input():
    schema = {"definitions": {"v1Thing": {"required": ["a", "b"]}}}
    result = relax_oneof_required(schema, {"v1Thing": {"a"}})
    assert result["definitions"]["v1Thing"]["required"] == ["b"]
    assert schema["definitions"]["v1Thing"]["required"] == ["a", "b"]


def _policy_schema() -> dict:
    ref = "#/components/schemas/"
    return {
        "paths": {
            "/policies/{id}": {
                "get": {
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": f"{ref}GetPolicyResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/policies": {
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"{ref}CreatePolicyRequest"}
                            }
                        }
                    },
                    "responses": {},
                }
            },
        },
        "components": {
            "schemas": {
                "GetPolicyResponse": {
                    "properties": {"policy": {"$ref": f"{ref}Settings"}},
                    "required": ["policy"],
                },
                "Settings": {
                    "properties": {
                        "baseline": {"$ref": f"{ref}Baseline"},
                        "mode": {"$ref": f"{ref}Mode"},
                        "name": {"type": "string"},
                        "rules": {"type": "array", "items": {"$ref": f"{ref}Baseline"}},
                    },
                    "required": ["baseline", "mode", "name", "rules"],
                },
                "Baseline": {"properties": {"x": {"type": "string"}}},
                "Mode": {"type": "string", "enum": ["A", "B"]},
                "CreatePolicyRequest": {
                    "properties": {"settings": {"$ref": f"{ref}Baseline"}},
                    "required": ["settings"],
                },
            }
        },
    }


def test_response_models_drop_message_fields_from_required():
    schemas = relax_response_message_required(_policy_schema())["components"]["schemas"]
    assert "required" not in schemas["GetPolicyResponse"]
    assert schemas["Settings"]["required"] == ["mode", "name", "rules"]


def test_request_only_models_keep_required_message_fields():
    original = _policy_schema()
    original["components"]["requestBodies"] = {"Body": {"required": True}}
    schemas = relax_response_message_required(original)["components"]["schemas"]
    assert schemas["CreatePolicyRequest"]["required"] == ["settings"]
    assert original["components"]["schemas"]["Settings"]["required"] == [
        "baseline",
        "mode",
        "name",
        "rules",
    ]


def test_proto_collisions_finds_stems_shared_across_compiled_folders(tmp_path):
    openapi_base, proto_base = tmp_path / "openapi", tmp_path / "proto"
    selected = {"alerting": [], "device": []}
    for service, folder, protos in [
        ("alerting", "alerting/public/v202505", ["mitigation", "alert"]),
        ("alerting", "alerting/types/v202506", ["mitigation", "sorting"]),
        ("device", "device/v202308beta1", ["device"]),
    ]:
        for proto in protos:
            path = proto_base / "kentik" / folder / f"{proto}.proto"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch()
        selected[service].append({"path": str(openapi_base / folder / "x.json")})

    assert _proto_collisions(selected, openapi_base, proto_base) == {
        "alerting": {"mitigation"},
        "device": set(),
    }


def test_pb_stem_qualifies_only_colliding_kentik_modules():
    collisions = {"alerting": {"mitigation"}}
    assert (
        _pb_stem("kentik.alerting.types.v202506", "mitigation", collisions)
        == "mitigation_types_v202506"
    )
    assert _pb_stem("kentik.alerting.public.v202505", "alert", collisions) == "alert"
    assert _pb_stem("kentik.ktbgp.v202501", "mitigation", collisions) == "mitigation"


def test_qualify_colliding_imports_resolves_by_package_not_name():
    content = (
        "from kentik.alerting.types.v202506 import mitigation_pb2 as _types\n"
        "from kentik.alerting.public.v202505 import mitigation_pb2 as _public\n"
        "from kentik.alerting.public.v202505 import common_pb2 as _common\n"
    )
    result = _qualify_colliding_imports(content, {"alerting": {"mitigation"}})
    assert result == (
        "from kentik.alerting.types.v202506 import mitigation_types_v202506_pb2 as _types\n"
        "from kentik.alerting.public.v202505 import mitigation_public_v202505_pb2 as _public\n"
        "from kentik.alerting.public.v202505 import common_pb2 as _common\n"
    )
    assert "import mitigation_public_v202505_pb2 as _public" in _rewrite_grpc_imports(
        result
    )


def _schemas(*names: str, **definitions: dict) -> dict:
    return {
        "components": {"schemas": {name: definitions.get(name, {}) for name in names}}
    }


def test_models_differing_only_by_case_fail_across_files_of_a_service():
    seen: dict = {}
    check_model_names(_schemas("DeviceLabel", "Device"), seen, "a.json")

    with pytest.raises(
        RuntimeError, match="`deviceLabel` differs from model `DeviceLabel`"
    ):
        check_model_names(_schemas("deviceLabel"), seen, "b.json")


def test_same_model_with_the_same_definition_in_two_files_passes():
    seen: dict = {}
    status = {"type": "object", "properties": {"code": {"type": "integer"}}}
    check_model_names(_schemas("rpcStatus", "Device", rpcStatus=status), seen, "a.json")
    check_model_names(_schemas("rpcStatus", rpcStatus=dict(status)), seen, "b.json")


def test_same_model_with_a_different_definition_fails():
    seen: dict = {}
    check_model_names(
        _schemas("Mitigation", Mitigation={"properties": {"id": {}}}), seen, "a.json"
    )

    with pytest.raises(RuntimeError, match="defined differently in a.json"):
        check_model_names(
            _schemas("Mitigation", Mitigation={"properties": {"name": {}}}),
            seen,
            "b.json",
        )


def test_rewrite_grpc_imports_keeps_google_imports_absolute():
    line = (
        "from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2\n"
    )
    assert _rewrite_grpc_imports(line) == line


def _pb_module(root: Path, service: str, name: str, *imports: str) -> Path:
    path = root / service / "pb" / f"{name}.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{line}\n" for line in imports), encoding="utf-8")
    return path


def test_relink_points_each_import_at_the_service_that_compiled_it(tmp_path: Path):
    owners = {
        ("kentik.user.v202405", "user_pb2"): "user",
        ("kentik.device.v202308", "device_pb2"): "device",
        ("kentik.device.v202308", "common_pb2"): "device",
    }
    _pb_module(tmp_path, "user", "user_pb2")
    module = _pb_module(
        tmp_path,
        "device",
        "device_pb2",
        "from kentik.user.v202405 import user_pb2 as _user",
        "from kentik.device.v202308 import common_pb2 as _common",
        "from google.api import annotations_pb2 as _ann",
    )

    _relink_pb2_dependency_imports(tmp_path, owners)

    assert module.read_text(encoding="utf-8").splitlines() == [
        "from kentik_api.gen.user.pb import user_pb2 as _user",
        "from . import common_pb2 as _common",
        "from google.api import annotations_pb2 as _ann",
    ]


def test_relink_fails_on_a_proto_version_nobody_compiled(tmp_path: Path):
    """Linking by module name alone would pick the user service's newer user_pb2."""
    owners = {("kentik.user.v202405", "user_pb2"): "user"}
    _pb_module(tmp_path, "user", "user_pb2")
    _pb_module(
        tmp_path,
        "device",
        "device_pb2",
        "from kentik.user.v202211 import user_pb2 as _user",
    )

    with pytest.raises(RuntimeError, match=r"kentik\.user\.v202211\.user_pb2"):
        _relink_pb2_dependency_imports(tmp_path, owners)


def _function_by_name(source: str, name: str) -> ast.FunctionDef | None:
    return next(
        (
            node
            for node in ast.walk(ast.parse(source))
            if isinstance(node, ast.FunctionDef) and node.name == name
        ),
        None,
    )


@pytest.mark.parametrize(
    "check", ["validate_schema_files_or_raise", "validate_selected_services_or_raise"]
)
def test_generate_modular_sdk_validates_schema_before_cleaning_output_dir(check):
    """The corrupted-checkout gates must run before SDK_OUTPUT_DIR is touched.

    Regression test: an earlier version of this gate ran *after* the
    "Cleaning old modules" step, so a validation failure still left
    src/kentik_api/gen/ wiped out. This was discovered by manually reproducing the
    2026-08-26 incident end-to-end rather than trusting fixture tests alone.
    Runs as a static/AST check (not a full generation) since
    generate_modular_sdk() shells out to git/protoc/uvx and isn't otherwise
    unit-tested in isolation.
    """
    source = (_scripts_dir / "generate_sdk.py").read_text(encoding="utf-8")
    select_node = _function_by_name(source, "_select_swagger_files")
    func_node = _function_by_name(source, "generate_modular_sdk")
    assert select_node is not None, "_select_swagger_files() not found"
    assert func_node is not None, "generate_modular_sdk() not found"

    def call_lines(node: ast.FunctionDef, name: str) -> list[int]:
        return [
            n.lineno
            for n in ast.walk(node)
            if isinstance(n, ast.Call) and ast.unparse(n.func).endswith(name)
        ]

    assert call_lines(select_node, check), f"{check}(...) call not found"
    select_lines = call_lines(func_node, "_select_swagger_files")
    rmtree_lines = call_lines(func_node, "rmtree")
    assert select_lines, "_select_swagger_files(...) call not found"
    assert rmtree_lines, "shutil.rmtree(...) call not found"
    assert max(select_lines) < min(rmtree_lines), (
        f"{check}() must run before shutil.rmtree() "
        "cleans SDK_OUTPUT_DIR, so a validation failure never leaves "
        "generated output partially wiped"
    )


def test_generated_doc_pages_are_the_pages_the_generator_owns():
    docs = PROJECT_ROOT / "docs" / "sphinx"
    assert set(GENERATED_DOC_PAGES) == {
        docs / "services",
        docs / "sdk_runtime_architecture.md",
    }


def test_generated_doc_pages_are_formatted_after_render_and_before_the_surface():
    """Ruff formats their Python blocks, so the CI Markdown check and drift check agree."""
    source = (_scripts_dir / "generate_sdk.py").read_text(encoding="utf-8")
    func_node = _function_by_name(source, "generate_modular_sdk")
    assert func_node is not None, "generate_modular_sdk() not found"

    calls = [n for n in ast.walk(func_node) if isinstance(n, ast.Call)]
    format_lines = [
        n.lineno
        for n in calls
        if ast.unparse(n.func) == "_format_generated"
        and "GENERATED_DOC_PAGES" in ast.unparse(n)
    ]
    render_lines = [n.lineno for n in calls if ast.unparse(n.func).endswith(".render")]
    surface_lines = [
        n.lineno for n in calls if ast.unparse(n.func) == "api_surface.generate"
    ]

    assert format_lines, "no ruff format call on GENERATED_DOC_PAGES"
    assert max(render_lines) < min(format_lines) < min(surface_lines)


def test_clean_schema_names_keeps_the_prefix_when_stripping_would_overwrite_a_schema():
    schema = {
        "definitions": {
            "AlertAcknowledgement": {
                "type": "object",
                "properties": {"state": {"type": "string"}},
            },
            "v202505AlertAcknowledgement": {"type": "string", "enum": ["A", "B"]},
            "v202505Alert": {
                "type": "object",
                "properties": {
                    "acknowledgement": {"$ref": "#/definitions/AlertAcknowledgement"},
                    "legacy": {"$ref": "#/definitions/v202505AlertAcknowledgement"},
                },
            },
        }
    }

    result = clean_schema_names(schema, "v202505")["definitions"]

    assert result["AlertAcknowledgement"]["type"] == "object"
    assert result["v202505AlertAcknowledgement"]["enum"] == ["A", "B"]
    assert "Alert" in result
    props = result["Alert"]["properties"]
    assert props["acknowledgement"]["$ref"].endswith("/AlertAcknowledgement")
    assert props["legacy"]["$ref"].endswith("/v202505AlertAcknowledgement")


def test_the_real_alert_schema_keeps_acknowledgement_an_object():
    import json

    swagger = (
        Path(__file__).resolve().parents[3]
        / "api-schema-public"
        / "gen"
        / "openapiv3"
        / "kentik"
        / "alerting"
        / "public"
        / "v202505"
        / "alert.swagger.json"
    )
    if not swagger.exists():
        pytest.skip("local api-schema-public checkout not available")

    result = clean_schema_names(
        json.loads(swagger.read_text(encoding="utf-8")), "v202505"
    )
    definitions = result["components"]["schemas"]

    assert definitions["AlertAcknowledgement"].get("type") == "object"
    assert "v202505AlertAcknowledgement" in definitions


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def _schema_repo(path: Path, commits: int = 1) -> list[str]:
    """A git repo with `commits` commits, oldest first."""
    path.mkdir()
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@example.invalid")
    _git(path, "config", "user.name", "t")
    shas = []
    for n in range(commits):
        (path / "schema.json").write_text(str(n), encoding="utf-8")
        _git(path, "add", "schema.json")
        _git(path, "commit", "-q", "-m", str(n))
        shas.append(_git(path, "rev-parse", "HEAD"))
    return shas


def test_the_committed_pin_is_one_commit_sha():
    assert len(read_schema_pin()) == 40


@pytest.mark.parametrize("content", ["", "HEAD", "9de9a68", "x" * 40])
def test_a_malformed_pin_is_rejected(tmp_path, content):
    pin = tmp_path / "schema.lock"
    pin.write_text(content, encoding="utf-8")

    with pytest.raises(ValueError, match="40-character commit SHA"):
        read_schema_pin(pin)


def test_a_missing_pin_names_the_command_that_writes_it(tmp_path):
    with pytest.raises(ValueError, match="uv run poe sync-schema"):
        read_schema_pin(tmp_path / "schema.lock")


def test_fetch_checks_out_the_pinned_commit_not_the_tip(tmp_path):
    upstream = tmp_path / "upstream"
    first, _ = _schema_repo(upstream, commits=2)
    # GitHub serves any reachable commit; a local repo needs this to match it.
    _git(upstream, "config", "uploadpack.allowAnySHA1InWant", "true")

    commit = fetch_schema(str(upstream), first, tmp_path / "checkout")

    assert commit == first
    assert (tmp_path / "checkout" / "schema.json").read_text() == "0"


def test_fetch_rejects_a_ref_git_would_read_as_an_option(tmp_path):
    with pytest.raises(ValueError, match="must not start with"):
        fetch_schema("https://example.invalid/r.git", "--upload-pack=x", tmp_path)


def test_a_clean_local_checkout_reports_its_commit(tmp_path):
    repo = tmp_path / "schema"
    (sha,) = _schema_repo(repo)
    (repo / "uv.lock").write_text("untracked", encoding="utf-8")

    assert local_schema_commit(repo) == sha


def test_a_modified_local_checkout_reports_no_commit(tmp_path):
    repo = tmp_path / "schema"
    _schema_repo(repo)
    (repo / "schema.json").write_text("edited", encoding="utf-8")

    assert local_schema_commit(repo) is None


def test_a_local_folder_outside_git_reports_no_commit(tmp_path):
    assert local_schema_commit(tmp_path) is None


def test_a_ref_with_a_local_schema_is_rejected(tmp_path):
    with (
        pytest.raises(ValueError, match="remote repository only"),
        get_schema_root(str(tmp_path), "HEAD"),
    ):
        pass


def _outputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    gen = tmp_path / "gen"
    (gen / "device").mkdir(parents=True)
    (gen / "device" / "wrapper.py").write_text("old", encoding="utf-8")
    mixin = tmp_path / "client_mixin.py"
    mixin.write_text("old", encoding="utf-8")
    return gen, mixin, tmp_path / "schema.lock"


def _half_build(gen: Path, mixin: Path, pin: Path) -> None:
    shutil.rmtree(gen)
    (gen / "user").mkdir(parents=True)
    mixin.write_text("new", encoding="utf-8")
    pin.write_text("new", encoding="utf-8")


@pytest.mark.parametrize("error", [RuntimeError, KeyboardInterrupt])
def test_a_failed_run_restores_every_output(tmp_path, error):
    gen, mixin, pin = _outputs(tmp_path)

    with pytest.raises(error), restored_on_failure((gen, mixin, pin)):
        _half_build(gen, mixin, pin)
        raise error

    assert sorted(p.name for p in gen.iterdir()) == ["device"]
    assert (gen / "device" / "wrapper.py").read_text() == "old"
    assert mixin.read_text() == "old"
    assert not pin.exists()


def test_a_completed_run_keeps_the_new_output(tmp_path):
    gen, mixin, pin = _outputs(tmp_path)

    with restored_on_failure((gen, mixin, pin)):
        _half_build(gen, mixin, pin)

    assert sorted(p.name for p in gen.iterdir()) == ["user"]
    assert mixin.read_text() == "new"
    assert pin.read_text() == "new"


def test_write_text_lf_writes_lf_on_every_os(tmp_path):
    from scripts.generation._shared import write_text_lf

    target = tmp_path / "out.md"
    write_text_lf(target, "a\nb é\n")

    assert target.read_bytes() == "a\nb é\n".encode()


def test_the_generator_writes_files_only_through_write_text_lf():
    # Path.write_text writes CRLF on Windows, which fails the drift check there.
    sources = [PROJECT_ROOT / "scripts" / "generate_sdk.py"]
    sources += sorted((PROJECT_ROOT / "scripts" / "generation").glob("*.py"))

    offenders = [
        f"{path.name}:{node.lineno}"
        for path in sources
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Attribute) and node.attr == "write_text"
    ]

    assert offenders == []


def test_a_failed_companion_compile_aborts_generation(tmp_path, monkeypatch):
    import generate_sdk

    vendor = tmp_path / "protovendor/github.com/grpc-ecosystem/grpc-gateway"
    vendor.mkdir(parents=True)
    monkeypatch.setattr(generate_sdk, "SDK_OUTPUT_DIR", tmp_path / "gen")

    def fail(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0], stderr="protoc failed")

    monkeypatch.setattr(generate_sdk.subprocess, "run", fail)

    with pytest.raises(subprocess.CalledProcessError):
        generate_sdk._compile_proto_companions(tmp_path)


def test_an_untracked_schema_input_reports_no_commit(tmp_path):
    repo = tmp_path / "schema"
    _schema_repo(repo)
    swagger = repo / "gen/openapiv3/kentik/new/v1/new.swagger.json"
    swagger.parent.mkdir(parents=True)
    swagger.write_text("{}", encoding="utf-8")

    assert local_schema_commit(repo) is None
