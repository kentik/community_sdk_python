# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Records the SDK's public API surface and diffs two recordings into release notes.

`uv run poe generate` writes `api_surface.json` at the repo root on every run. Because that
file is committed alongside the generated code, any two points in history can be
compared with a single `git show <ref>:api_surface.json`, instead of reconstructing
whole generated trees. `scripts/release_notes.py` does exactly that.

Nothing here records timestamps or versions of the generator itself. Those would
change on every run and bury the real signal under noise.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import tomllib
from pathlib import Path
from typing import Any

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name
from packaging.version import Version

from ._shared import (
    PROJECT_ROOT,
    SDK_OUTPUT_DIR,
    discover_service_model_classes,
    grpc_call,
    grpc_stub_services,
    iter_service_dirs,
    parse_generated_rest_module,
    write_text_lf,
)

SURFACE_FILE = PROJECT_ROOT / "api_surface.json"
SCHEMA_VERSION = 8

_LEGACY_REQUIREMENTS = ("grpcio", "protobuf", "httpx", "pydantic")
_PROTOBUF_GENCODE_RE = re.compile(
    r"ValidateProtobufRuntimeVersion\(\s*_runtime_version\.Domain\.\w+,\s*(\d+),\s*(\d+),\s*(\d+),"
)
_GRPC_GENCODE_RE = re.compile(r'^GRPC_GENERATED_VERSION\s*=\s*"([^"]+)"', re.MULTILINE)


def _operation_key(method: str, path: str) -> str:
    """Identifies an operation by method and path.

    Never by operationId alone: multi-file services legitimately reuse generic ids
    such as `List` across different underlying REST modules.
    """
    return f"{method.upper()} {path}"


def _declared_requirements() -> dict[str, str]:
    """Every runtime dependency, plus the Python floor as `python`."""
    project = tomllib.loads(
        (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )["project"]
    found: dict[str, str] = {
        canonicalize_name(Requirement(spec).name): spec
        for spec in project["dependencies"]
    }
    if "requires-python" in project:
        found["python"] = f"python{project['requires-python']}"
    return dict(sorted(found.items()))


def _gencode_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for stub in SDK_OUTPUT_DIR.rglob("*_pb2.py"):
        match = _PROTOBUF_GENCODE_RE.search(stub.read_text(encoding="utf-8"))
        if match:
            versions["protobuf"] = ".".join(match.groups())
            break
    for stub in SDK_OUTPUT_DIR.rglob("*_pb2_grpc.py"):
        match = _GRPC_GENCODE_RE.search(stub.read_text(encoding="utf-8"))
        if match:
            versions["grpcio"] = match.group(1)
            break
    return versions


def _mounted_services() -> set[str]:
    mixin = PROJECT_ROOT / "src" / "kentik_api" / "client_mixin.py"
    if not mixin.exists():
        return set()
    return set(
        re.findall(r"from kentik_api\.gen\.(\w+)\.services\.", mixin.read_text("utf-8"))
    )


def _rest_only_services() -> set[str]:
    """Services the mixin mounts on the V5 REST transport, whatever the protocol."""
    mixin = PROJECT_ROOT / "src" / "kentik_api" / "client_mixin.py"
    if not mixin.exists():
        return set()
    return set(
        re.findall(
            r"self\.(\w+) = \w+\(self\._v5_transport\)", mixin.read_text("utf-8")
        )
    )


def is_rest_only(service: dict[str, Any]) -> bool:
    """A record before schema_version 8 has no flag, and had no REST-only service."""
    return service.get("rest_only", False)


def _is_required(value: ast.expr | None) -> bool:
    """A field is required when `Field(...)` gives it no default."""
    if not isinstance(value, ast.Call):
        return value is None
    return not value.args and not any(
        kw.arg in ("default", "default_factory") for kw in value.keywords
    )


def _model_shapes(service_dir: Path) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """Reads each model's fields and each enum's members from the generated source.

    Parsed, never imported: the generator does not execute generated code.
    """
    fields: dict[str, Any] = {}
    enums: dict[str, list[str]] = {}
    for model_file in sorted((service_dir / "models").glob("*.py")):
        tree = ast.parse(model_file.read_text(encoding="utf-8"))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            if any(ast.unparse(base) == "Enum" for base in node.bases):
                enums[node.name] = [
                    target.id
                    for stmt in node.body
                    if isinstance(stmt, ast.Assign)
                    for target in stmt.targets
                    if isinstance(target, ast.Name)
                ]
                continue
            fields[node.name] = {
                stmt.target.id: {
                    "type": ast.unparse(stmt.annotation),
                    "required": _is_required(stmt.value),
                }
                for stmt in node.body
                if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name)
            }
    return dict(sorted(fields.items())), dict(sorted(enums.items()))


def _wrapper_method_by_rest_call(
    service_dir: Path,
) -> dict[tuple[str, str], tuple[str, str | None]]:
    """Maps (REST module, REST function) to the client method and its gRPC route.

    The route is None when the method raises NotImplementedError on gRPC.
    """
    wrapper = service_dir / "services" / f"{service_dir.name}.py"
    if not wrapper.exists():
        return {}
    tree = ast.parse(wrapper.read_text(encoding="utf-8"))
    modules = {
        alias.asname: alias.name.rsplit(".", 1)[-1]
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.asname
    }
    methods: dict[tuple[str, str], tuple[str, str | None]] = {}
    for cls in (node for node in tree.body if isinstance(node, ast.ClassDef)):
        init = next(
            (
                fn
                for fn in cls.body
                if isinstance(fn, ast.FunctionDef) and fn.name == "__init__"
            ),
            None,
        )
        stubs = grpc_stub_services(init) if init else {}
        for fn in cls.body:
            if not isinstance(fn, ast.FunctionDef) or fn.name.startswith("_"):
                continue
            route = grpc_call(fn, stubs)
            for call in ast.walk(fn):
                if (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Attribute)
                    and isinstance(call.func.value, ast.Name)
                    and call.func.value.id in modules
                ):
                    methods[(modules[call.func.value.id], call.func.attr)] = (
                        fn.name,
                        route.rpc if route else None,
                    )
    return methods


def _error_responses(service_dir: Path) -> dict[str, dict[str, str]]:
    """Maps each operation error class to its per-status classes, as `response_error_map` sets them."""
    error_file = service_dir / "error" / "__init__.py"
    if not error_file.exists():
        return {}
    responses: dict[str, dict[str, str]] = {}
    for node in ast.parse(error_file.read_text(encoding="utf-8")).body:
        if not (
            isinstance(node, ast.Assign)
            and isinstance(target := node.targets[0], ast.Attribute)
            and target.attr == "response_error_map"
            and isinstance(target.value, ast.Name)
            and isinstance(node.value, ast.Dict)
        ):
            continue
        responses[target.value.id] = {
            key.value: value.id
            for key, value in zip(node.value.keys, node.value.values, strict=True)
            if isinstance(key, ast.Constant)
            and isinstance(key.value, str)
            and isinstance(value, ast.Name)
        }
    return responses


def capture(output_dir: Path | None = None) -> dict[str, Any]:
    """Builds a snapshot of the generated SDK's public surface."""
    root = SDK_OUTPUT_DIR if output_dir is None else output_dir
    mounted = _mounted_services()
    rest_only = _rest_only_services()
    services: dict[str, Any] = {}

    for service_dir in iter_service_dirs(root):
        wrapper_methods = _wrapper_method_by_rest_call(service_dir)
        error_responses = _error_responses(service_dir)
        operations: dict[str, Any] = {}
        for module in sorted((service_dir / "services").glob("*.py")):
            for op in parse_generated_rest_module(module):
                method, route = wrapper_methods.get(
                    (module.stem, op.name), (None, None)
                )
                operations[_operation_key(op.http_method, op.path)] = {
                    "operation": op.operation_name,
                    "method": method,
                    "grpc": route,
                    "status": op.expected_status,
                    "required_params": sorted(
                        name for name, _, required in op.params if required
                    ),
                    "params": {name: annotation for name, annotation, _ in op.params},
                    "returns": op.return_type,
                    "error": op.error_cls_name,
                    "error_responses": error_responses.get(op.error_cls_name, {}),
                }

        fields, enums = _model_shapes(service_dir)
        services[service_dir.name] = {
            "mounted": service_dir.name in mounted,
            "rest_only": service_dir.name in rest_only,
            "operations": dict(sorted(operations.items())),
            "models": sorted(discover_service_model_classes(service_dir)),
            "fields": fields,
            "enums": enums,
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "requirements": _declared_requirements(),
        "gencode": _gencode_versions(),
        "services": dict(sorted(services.items())),
    }


def write(surface: dict[str, Any], path: Path | None = None) -> Path:
    target = SURFACE_FILE if path is None else path
    write_text_lf(target, json.dumps(surface, indent=2) + "\n")
    return target


def read(path: Path | None = None) -> dict[str, Any]:
    target = SURFACE_FILE if path is None else path
    return json.loads(target.read_text(encoding="utf-8"))


def recorded_at(ref: str) -> dict[str, Any] | None:
    """Returns the surface committed at a git ref, or None if it has no record."""
    result = subprocess.run(
        ["git", "show", f"{ref}:{SURFACE_FILE.name}"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return json.loads(result.stdout) if result.returncode == 0 else None


def diff(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Compares two surface snapshots into an ordered, render-ready delta."""
    old_services, new_services = before.get("services", {}), after.get("services", {})

    added = sorted(set(new_services) - set(old_services))
    removed = sorted(set(old_services) - set(new_services))

    changed: dict[str, Any] = {}
    for name in sorted(set(old_services) & set(new_services)):
        old, new = old_services[name], new_services[name]
        entry = {
            "added_operations": sorted(set(new["operations"]) - set(old["operations"])),
            "removed_operations": sorted(
                set(old["operations"]) - set(new["operations"])
            ),
            "added_models": sorted(set(new["models"]) - set(old["models"])),
            "removed_models": sorted(set(old["models"]) - set(new["models"])),
            "mount_changed": old["mounted"] != new["mounted"],
            "now_mounted": new["mounted"],
            "changed_operations": _changed_operations(
                old["operations"], new["operations"]
            ),
            **_member_changes(old, new),
        }
        if any(v for k, v in entry.items() if k != "now_mounted"):
            changed[name] = entry

    return {
        "added_services": [
            {
                "name": name,
                "mounted": new_services[name]["mounted"],
                "operations": sorted(new_services[name]["operations"]),
                "models": new_services[name]["models"],
            }
            for name in added
        ],
        "removed_services": removed,
        "changed_services": changed,
        "requirements": _diff_mapping(
            before.get("requirements", {}), _comparable_requirements(before, after)
        ),
        "gencode": _diff_mapping(before.get("gencode", {}), after.get("gencode", {})),
    }


def _comparable_requirements(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, str]:
    """After's requirements, minus ones an older record never tracked.

    Without this, every untracked dependency would read as newly required.
    """
    requirements = after.get("requirements", {})
    if before.get("schema_version", 0) >= 6:
        return requirements
    return {k: v for k, v in requirements.items() if k in _LEGACY_REQUIREMENTS}


def _bounds(specifier: SpecifierSet) -> tuple[Version | None, Version | None, set[str]]:
    """Approximate floor, cap, and excluded versions of a specifier set."""
    low = high = None
    excluded = set()
    for spec in specifier:
        if spec.operator == "!=":
            excluded.add(spec.version)
            continue
        if spec.operator == "===":
            continue
        version = Version(spec.version.removesuffix(".*"))
        if spec.operator in (">=", ">", "~=", "=="):
            low = version if low is None else max(low, version)
        if spec.operator in ("<", "<=", "=="):
            high = version if high is None else min(high, version)
    return low, high, excluded


def _narrowed(before: str, after: str) -> bool:
    """True when `after` can reject a version or environment `before` accepted."""
    old, new = Requirement(before), Requirement(after)
    if (old.extras, str(old.marker)) != (new.extras, str(new.marker)):
        return True
    old_low, old_high, old_excluded = _bounds(old.specifier)
    new_low, new_high, new_excluded = _bounds(new.specifier)
    return (
        (new_low is not None and (old_low is None or new_low > old_low))
        or (new_high is not None and (old_high is None or new_high < old_high))
        or bool(new_excluded - old_excluded)
    )


def _changed_operations(
    before: dict[str, Any], after: dict[str, Any]
) -> list[dict[str, Any]]:
    changes = []
    for key in sorted(set(before) & set(after)):
        old, new = before[key], after[key]
        old_required = set(old.get("required_params", []))
        new_required = set(new.get("required_params", []))
        # A record from before schema_version 3 has no signature, so it compares
        # as unchanged rather than as every parameter added.
        old_params, new_params = old.get("params"), new.get("params", {})
        removed_params, retyped_params, return_change = [], [], None
        if old_params is not None:
            removed_params = sorted(set(old_params) - set(new_params))
            retyped_params = [
                {"name": p, "before": old_params[p], "after": new_params[p]}
                for p in sorted(set(old_params) & set(new_params))
                if old_params[p] != new_params[p]
            ]
            if old.get("returns") != new.get("returns"):
                return_change = [old.get("returns"), new.get("returns")]
        # Before schema_version 4 a record has no method; a service with no
        # wrapper has None. Neither is a rename.
        old_method, new_method = old.get("method"), new.get("method")
        method_change = (
            [old_method, new_method]
            if old_method and new_method and old_method != new_method
            else None
        )
        # Before schema_version 5 a record has no route key.
        old_route, new_route = old.get("grpc"), new.get("grpc")
        grpc_change = (
            [old_route, new_route] if "grpc" in old and old_route != new_route else None
        )
        # Before schema_version 7 a record has no error classes.
        error_change, removed_errors, added_errors = None, [], []
        if "error" in old:
            if old["error"] != new["error"]:
                error_change = [old["error"], new["error"]]
            old_errors, new_errors = old["error_responses"], new["error_responses"]
            removed_errors = sorted(
                old_errors[status] for status in set(old_errors) - set(new_errors)
            )
            added_errors = sorted(
                new_errors[status] for status in set(new_errors) - set(old_errors)
            )
        if (
            old.get("status") == new.get("status")
            and old_required == new_required
            and not removed_params
            and not retyped_params
            and return_change is None
            and method_change is None
            and grpc_change is None
            and error_change is None
            and not removed_errors
            and not added_errors
        ):
            continue
        changes.append(
            {
                "operation": key,
                "status": [old.get("status"), new.get("status")],
                "newly_required": sorted(new_required - old_required),
                "no_longer_required": sorted(old_required - new_required),
                "removed_params": removed_params,
                "retyped_params": retyped_params,
                "return_change": return_change,
                "method_change": method_change,
                "grpc_change": grpc_change,
                "error_change": error_change,
                "removed_errors": removed_errors,
                "added_errors": added_errors,
            }
        )
    return changes


def _member_changes(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """Field and enum member changes in models that exist on both sides.

    A record from before schema_version 2 has no members, so it compares as
    unchanged rather than as every field added.
    """
    if "fields" not in old or "enums" not in old:
        return {}
    added, removed, retyped = [], [], []
    for model in sorted(set(old["fields"]) & set(new["fields"])):
        before, after = old["fields"][model], new["fields"][model]
        for field in sorted(set(after) - set(before)):
            added.append({"name": f"{model}.{field}", **after[field]})
        removed += [f"{model}.{field}" for field in sorted(set(before) - set(after))]
        for field in sorted(set(before) & set(after)):
            if before[field] != after[field]:
                retyped.append(
                    {
                        "name": f"{model}.{field}",
                        "before": before[field],
                        "after": after[field],
                    }
                )
    added_values, removed_values = [], []
    for enum in sorted(set(old["enums"]) & set(new["enums"])):
        before, after = set(old["enums"][enum]), set(new["enums"][enum])
        added_values += [f"{enum}.{value}" for value in sorted(after - before)]
        removed_values += [f"{enum}.{value}" for value in sorted(before - after)]
    return {
        "added_fields": added,
        "removed_fields": removed,
        "changed_fields": retyped,
        "added_enum_values": added_values,
        "removed_enum_values": removed_values,
    }


def _describe(field: dict[str, Any]) -> str:
    return f"`{field['type']}`{', required' if field['required'] else ''}"


def breaking_changes(delta: dict[str, Any]) -> list[tuple[str, str]]:
    """Lists each change that can break a caller, as (message, name).

    `name` is what a CHANGELOG entry for the change must mention, so
    `release_notes.py --check-changelog` can tell whether it was written up.
    """
    breaking = [
        (f"- Service removed: `client.{name}`", name)
        for name in delta["removed_services"]
    ]
    for name, entry in delta["changed_services"].items():
        for operation in entry["removed_operations"]:
            breaking.append(
                (f"- `{name}`: operation removed, `{operation}`", operation.split()[-1])
            )
        if entry["mount_changed"] and not entry["now_mounted"]:
            breaking.append((f"- `client.{name}` is no longer available", name))
        for model in entry["removed_models"]:
            breaking.append((f"- `{name}`: model removed, `{model}`", model))
        for change in entry.get("changed_operations", []):
            if change.get("method_change"):
                before, after = change["method_change"]
                breaking.append(
                    (
                        (
                            f"- `{name}`: `{change['operation']}` is now "
                            f"`client.{name}.{after}`, not `{before}`"
                        ),
                        before,
                    )
                )
            if change.get("grpc_change") and change["grpc_change"][0]:
                before, after = change["grpc_change"]
                breaking.append(
                    (
                        f"- `{name}`: `{change['operation']}` no longer routes to "
                        f"gRPC `{before}`" + (f", now `{after}`" if after else ""),
                        before,
                    )
                )
            for param in change["newly_required"]:
                breaking.append(
                    (
                        f"- `{name}`: `{change['operation']}` now requires `{param}`",
                        param,
                    )
                )
            for param in change.get("removed_params", []):
                breaking.append(
                    (
                        f"- `{name}`: `{change['operation']}` no longer accepts `{param}`",
                        param,
                    )
                )
            for retyped in change.get("retyped_params", []):
                breaking.append(
                    (
                        (
                            f"- `{name}`: `{change['operation']}` parameter "
                            f"`{retyped['name']}` changed from `{retyped['before']}` "
                            f"to `{retyped['after']}`"
                        ),
                        retyped["name"],
                    )
                )
            if change.get("return_change"):
                before, after = change["return_change"]
                breaking.append(
                    (
                        (
                            f"- `{name}`: `{change['operation']}` now returns `{after}`, "
                            f"not `{before}`"
                        ),
                        after,
                    )
                )
            if change.get("error_change"):
                before, after = change["error_change"]
                breaking.append(
                    (
                        (
                            f"- `{name}`: `{change['operation']}` raises `{after}`, "
                            f"not `{before}`"
                        ),
                        before,
                    )
                )
            for error in change.get("removed_errors", []):
                breaking.append((f"- `{name}`: error class removed, `{error}`", error))
        for field in entry.get("added_fields", []):
            if field["required"]:
                breaking.append(
                    (f"- `{name}`: new required field `{field['name']}`", field["name"])
                )
        for field in entry.get("removed_fields", []):
            breaking.append((f"- `{name}`: field removed, `{field}`", field))
        for change in entry.get("changed_fields", []):
            before, after = change["before"], change["after"]
            if before["type"] == after["type"] and not (
                after["required"] and not before["required"]
            ):
                continue  # only became optional
            breaking.append(
                (
                    (
                        f"- `{name}`: `{change['name']}` changed from "
                        f"{_describe(change['before'])} to {_describe(change['after'])}"
                    ),
                    change["name"],
                )
            )
        for value in entry.get("removed_enum_values", []):
            breaking.append((f"- `{name}`: enum value removed, `{value}`", value))
    for package, change in delta["requirements"].items():
        if change["before"] is None:
            breaking.append(
                (f"- New required dependency, `{change['after']}`", package)
            )
        elif change["after"] is not None and _narrowed(
            change["before"], change["after"]
        ):
            breaking.append(
                (
                    (
                        f"- Dependency requirement narrowed, `{change['before']}` "
                        f"to `{change['after']}`"
                    ),
                    package,
                )
            )
    return breaking


def _diff_mapping(before: dict[str, str], after: dict[str, str]) -> dict[str, Any]:
    changes = {}
    for key in sorted(set(before) | set(after)):
        old, new = before.get(key), after.get(key)
        if old != new:
            changes[key] = {"before": old, "after": new}
    return changes


def is_empty(delta: dict[str, Any]) -> bool:
    return not any(delta.values())


def _service_bullets(entry: dict[str, Any]) -> list[str]:
    bullets = [f"  - added `{op}`" for op in entry["added_operations"]]
    bullets += [f"  - **removed** `{op}`" for op in entry["removed_operations"]]
    if entry["mount_changed"]:
        state = "now mounted on" if entry["now_mounted"] else "**no longer on**"
        bullets.append(f"  - {state} the client")
    if entry["added_models"]:
        count = len(entry["added_models"])
        bullets.append(
            f"  - {count} new model{'s' if count != 1 else ''}: "
            + ", ".join(f"`{m}`" for m in entry["added_models"][:5])
            + (" ..." if count > 5 else "")
        )
    for change in entry.get("changed_operations", []):
        if change.get("method_change"):
            before, after = change["method_change"]
            bullets.append(
                f"  - **`{change['operation']}` renamed**: `{before}` to `{after}`"
            )
        if change.get("grpc_change"):
            before, after = change["grpc_change"]
            bullets.append(
                f"  - `{change['operation']}` routes to gRPC `{after}`"
                if before is None
                else f"  - **`{change['operation']}` gRPC route**: `{before}` to `{after}`"
            )
        old_status, new_status = change["status"]
        if old_status != new_status:
            bullets.append(
                f"  - `{change['operation']}` succeeds with {new_status}, not {old_status}"
            )
        for param in change["newly_required"]:
            bullets.append(f"  - `{change['operation']}` now requires `{param}`")
        for param in change["no_longer_required"]:
            bullets.append(f"  - `{change['operation']}` no longer requires `{param}`")
        for param in change.get("removed_params", []):
            bullets.append(
                f"  - **`{change['operation']}` no longer accepts `{param}`**"
            )
        for retyped in change.get("retyped_params", []):
            bullets.append(
                f"  - **`{change['operation']}` parameter `{retyped['name']}`**: "
                f"`{retyped['before']}` to `{retyped['after']}`"
            )
        if change.get("return_change"):
            before, after = change["return_change"]
            bullets.append(
                f"  - **`{change['operation']}` now returns** `{after}`, not `{before}`"
            )
        if change.get("error_change"):
            before, after = change["error_change"]
            bullets.append(
                f"  - **`{change['operation']}` raises** `{after}`, not `{before}`"
            )
        for error in change.get("removed_errors", []):
            bullets.append(f"  - **error class removed**, `{error}`")
        for error in change.get("added_errors", []):
            bullets.append(f"  - error class added, `{error}`")
    for field in entry.get("added_fields", []):
        bullets.append(f"  - field added, `{field['name']}` ({_describe(field)})")
    for field in entry.get("removed_fields", []):
        bullets.append(f"  - **field removed**, `{field}`")
    for change in entry.get("changed_fields", []):
        bullets.append(
            f"  - `{change['name']}`: {_describe(change['before'])} to "
            f"{_describe(change['after'])}"
        )
    bullets += [
        f"  - enum value added, `{value}`"
        for value in entry.get("added_enum_values", [])
    ]
    bullets += [
        f"  - **enum value removed**, `{value}`"
        for value in entry.get("removed_enum_values", [])
    ]
    return bullets


def render_markdown(delta: dict[str, Any], *, since: str) -> str:
    """Renders a delta as GitHub-release-ready markdown."""
    if is_empty(delta):
        return f"No public API surface changes since `{since}`.\n"

    lines: list[str] = []

    breaking = [message for message, _ in breaking_changes(delta)]
    if breaking:
        lines += ["### Breaking changes\n", *dict.fromkeys(breaking), ""]

    if delta["added_services"]:
        lines.append("### New services\n")
        for service in delta["added_services"]:
            mount = (
                f"`client.{service['name']}`"
                if service["mounted"]
                else "types only, not mounted on the client"
            )
            ops, models = len(service["operations"]), len(service["models"])
            lines.append(
                f"- **{service['name']}** ({mount}): "
                f"{ops} operation{'s' if ops != 1 else ''}, "
                f"{models} model{'s' if models != 1 else ''}"
            )
            for operation in service["operations"]:
                lines.append(f"  - `{operation}`")
        lines.append("")

    endpoint_lines: list[str] = []
    for name, entry in delta["changed_services"].items():
        bullets = _service_bullets(entry)
        if bullets:
            endpoint_lines.append(f"- **{name}**")
            endpoint_lines.extend(bullets)
    if endpoint_lines:
        lines += ["### Changed services\n", *endpoint_lines, ""]

    if delta["requirements"]:
        lines.append("### Dependency requirements\n")
        for package, change in delta["requirements"].items():
            if change["before"] is None:
                lines.append(f"- `{package}` is now required: `{change['after']}`")
            elif change["after"] is None:
                lines.append(f"- `{package}` is no longer required")
            else:
                lines.append(
                    f"- `{package}`: `{change['before']}` to `{change['after']}`"
                )
        lines.append("")

    if delta["gencode"]:
        lines.append("### Generated protobuf toolchain\n")
        for package, change in delta["gencode"].items():
            lines.append(
                f"- `{package}` gencode: `{change['before']}` to `{change['after']}`"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


_RULE = "=" * 72


def render_regeneration_alert(
    before: dict[str, Any] | None, after: dict[str, Any]
) -> str:
    """Tells whoever ran `uv run poe generate` what changed and what they must do next.

    Release notes are not written here: they are cut at release time from the
    committed record, so this only says the CHANGELOG needs the change.
    """
    if before is None:
        return (
            "\nNo api_surface.json is committed at HEAD, so this run cannot say "
            "what changed.\nCompare against an earlier ref with "
            "`uv run poe release-notes --since <ref>`.\n"
        )
    delta = diff(before, after)
    if is_empty(delta):
        return "\nAPI surface unchanged since HEAD. No CHANGELOG entry is needed.\n"

    breaking = breaking_changes(delta)
    headline = (
        f"{len(breaking)} BREAKING change{'s' if len(breaking) != 1 else ''}"
        if breaking
        else "no breaking changes"
    )
    return "\n".join(
        [
            "",
            _RULE,
            f"⚠️  API SURFACE CHANGED since HEAD: {headline}",
            _RULE,
            render_markdown(delta, since="HEAD").rstrip(),
            _RULE,
            "Before you commit this regeneration, update the release notes:",
            "  1. Describe each change above in CHANGELOG.md, under ## Unreleased.",
            "     Name every breaking change exactly as listed above.",
            "  2. uv run poe check-changelog --since HEAD   # fails if one is not named",
            "  3. uv run poe release-notes --since HEAD     # preview what the release lists",
            "  4. Commit api_surface.json, the regenerated code, and CHANGELOG.md.",
            'Steps: "Update the release notes after every regeneration" in',
            "docs/sphinx/guides/generation.md.",
            _RULE,
            "",
        ]
    )


def render_summary(surface: dict[str, Any]) -> str:
    """Renders the whole surface, for the first release where no baseline exists yet."""
    services = surface.get("services", {})
    mounted = {name: s for name, s in services.items() if s["mounted"]}
    operations = sum(len(s["operations"]) for s in services.values())
    models = sum(len(s["models"]) for s in services.values())

    lines = [
        "### API surface",
        "",
        f"- {len(services)} services ({len(mounted)} mounted on the client)",
        f"- {operations} REST operations",
        f"- {models} models",
        "",
        "<details>",
        "<summary>Services</summary>",
        "",
    ]
    for name, service in services.items():
        count = len(service["operations"])
        detail = (
            f"`client.{name}`, {count} operation{'s' if count != 1 else ''}"
            if service["mounted"]
            else "types only, not mounted on the client"
        )
        lines.append(f"- **{name}**: {detail}")
    lines += ["", "</details>", ""]

    if surface.get("requirements"):
        lines += ["### Requires", ""]
        lines += [f"- `{spec}`" for spec in surface["requirements"].values()]
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def generate() -> Path:
    """Phase entrypoint: records the current surface. Called once per generation run."""
    return write(capture())
