# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Generated-code post-processing: import patching, model init rebuild, file cleanup.

Called once per service directory by generate_modular_sdk() after all swagger
files for the service have been generated, outside the schema availability window.
"""

import re
import textwrap
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel

from ._shared import discover_service_model_classes, normalize_symbol, write_text_lf


def fix_generated_service(service_dir: Path) -> None:
    """Applies all post-processing fixups to a freshly generated service directory."""
    model_classes = discover_service_model_classes(service_dir)
    _rebuild_models_init(service_dir)
    _fix_wildcard_exports(service_dir)
    _patch_service_files(service_dir, model_classes)


def _rebuild_models_init(service_dir: Path) -> None:
    """Rebuilds models/__init__.py from a full directory scan.

    openapi-python-generator overwrites models/__init__.py on each invocation,
    keeping only the last-processed swagger file's models. Rebuilding from a
    full scan keeps every class explicitly bound regardless of how many swagger
    files contributed to the service.
    """
    models_dir = service_dir / "models"
    if not models_dir.exists():
        return
    init_lines = []
    for model_file in sorted(models_dir.glob("*.py")):
        if model_file.name == "__init__.py":
            continue
        classes = re.findall(
            r"^class\s+([A-Za-z0-9_]+)",
            model_file.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if not classes:
            continue
        exports = ", ".join(f"{c} as {c}" for c in classes)
        init_lines.append(f"from .{model_file.stem} import {exports}")
    write_text_lf(
        models_dir / "__init__.py",
        "\n".join(init_lines) + ("\n" if init_lines else ""),
    )


def _fix_wildcard_exports(service_dir: Path) -> None:
    """Replaces `from .module import *` with explicit named imports in __init__.py files."""
    for init_file in service_dir.rglob("__init__.py"):
        if "error" in init_file.relative_to(service_dir).parts:
            continue
        content = init_file.read_text(encoding="utf-8")
        new_lines = []
        for line in content.splitlines():
            match = re.match(r"^from \.([a-zA-Z0-9_]+) import \*$", line)
            if match:
                module_name = match.group(1)
                target_py = init_file.parent / f"{module_name}.py"
                if target_py.exists():
                    target_content = target_py.read_text(encoding="utf-8")
                    classes = re.findall(
                        r"^class\s+([A-Za-z0-9_]+)",
                        target_content,
                        flags=re.MULTILINE,
                    )
                    if classes:
                        explicit_imports = ", ".join([f"{c} as {c}" for c in classes])
                        new_lines.append(
                            f"from .{module_name} import {explicit_imports}"
                        )
                        continue
            new_lines.append(line)
        write_text_lf(init_file, "\n".join(new_lines) + "\n")


def _patch_service_files(service_dir: Path, model_classes: set[str]) -> None:
    """Two passes: (1) filesystem cleanup, (2) ordered content transforms."""
    _cleanup_service_files(service_dir)

    transforms: list[Callable[[str], str]] = [
        _fix_import_aliases,
        _fix_pydantic_construct,
        _fix_path_parameters,
        _inject_data_body,
        _fix_typing_wildcard,
        _fix_model_field_names,
        _make_models_import_transform(model_classes),
        _alias_shadowed_typing_names,
        _dedupe_top_level_function_names,
        _normalize_triple_quoted_docstrings,
    ]

    for py_file in service_dir.rglob("*.py"):
        if _is_pb_or_error(py_file, service_dir):
            continue
        content = py_file.read_text(encoding="utf-8")
        for transform in transforms:
            content = transform(content)
        write_text_lf(py_file, content)


def _is_pb_or_error(py_file: Path, service_dir: Path) -> bool:
    return not {"pb", "error"}.isdisjoint(py_file.relative_to(service_dir).parts)


def _cleanup_service_files(service_dir: Path) -> None:
    """Deletes unwanted generated files and renames mangled service file names."""
    for py_file in list(service_dir.rglob("*.py")):
        if _is_pb_or_error(py_file, service_dir):
            continue
        if py_file.name.startswith("async_") or py_file.name == "api_config.py":
            py_file.unlink()
            continue
        if "Service_service" in py_file.name or "_service" in py_file.name.lower():
            clean_name = (
                py_file.name.replace("Service_service", "Service")
                .replace("_service_service", "Service")
                .replace("_service", "Service")
            )
            clean_name = clean_name[:1].upper() + clean_name[1:]
            py_file.rename(py_file.with_name(clean_name))


def _fix_import_aliases(content: str) -> str:
    """Rewrites generated api_config imports to the hand-written package paths."""
    content = re.sub(
        r"from \.*api_config import APIConfig, HTTPException",
        "from kentik_api.core.api_config import APIConfig\nfrom kentik_api.errors import HTTPException",
        content,
    )
    content = re.sub(
        r"from \.*api_config import APIConfig as APIConfig",
        "from kentik_api.core.api_config import APIConfig",
        content,
    )
    content = re.sub(
        r"from \.*api_config import HTTPException as HTTPException",
        "from kentik_api.errors import HTTPException",
        content,
    )
    return content


def _fix_pydantic_construct(content: str) -> str:
    """Upgrades v1-style `Model(**body)` instantiation to Pydantic v2 `model_construct`."""
    return re.sub(
        r"return ([A-Za-z0-9_]+)\(\*\*body\) if body.*? else \1\(\)",
        r"return \1(**body) if body is not None else \1.model_construct()",
        content,
    )


_PATH_PLACEHOLDER = re.compile(r"\{([^{}]+)\}")
_REQUEST_JSON_IMPORT = "from kentik_api.core.rest_runtime import request_json\n"


def _fix_path_parameters(content: str) -> str:
    """Encodes each path placeholder: {device.id} -> {path_segment(deviceid)}.

    The swagger names a placeholder by its proto field path; the generated
    argument is that path made a Python name, so `{from}` is `from_`.
    """
    fixed = re.sub(
        r"path\s*=\s*f[\"'].*?[\"']",
        lambda m: _PATH_PLACEHOLDER.sub(
            lambda p: f"{{path_segment({normalize_symbol(p.group(1))})}}", m.group(0)
        ),
        content,
    )
    if fixed == content:
        return content
    if _REQUEST_JSON_IMPORT not in fixed:
        raise ValueError(
            "_fix_path_parameters: path_segment is imported next to "
            f"{_REQUEST_JSON_IMPORT.strip()!r}, which this module lacks"
        )
    # A line of its own, because inject_service_error_handling() matches the
    # request_json import line's exact text.
    return fixed.replace(
        _REQUEST_JSON_IMPORT,
        "from kentik_api.core.rest_runtime import path_segment\n"
        + _REQUEST_JSON_IMPORT,
        1,
    )


# Only the fields the caller set: grpc-gateway builds a PATCH's update mask from
# the body keys, so a null for every unset field would clear them all.
_BODY_DUMP = "data.model_dump(by_alias=True, exclude_unset=True)"


def _inject_data_body(content: str) -> str:
    """Injects json_body=<_BODY_DUMP> into request_json() calls that have a data param."""
    functions = re.split(r"^(?=async def |def )", content, flags=re.MULTILINE)
    fixed_funcs = []
    for func in functions:
        if not func.strip():
            fixed_funcs.append(func)
            continue
        sig_part = func.split("->")[0] if "->" in func else func.split(":\n")[0]
        has_data_param = re.search(r"\bdata\s*:", sig_part) is not None
        has_json_kwarg = "json=" in func
        has_json_body_kwarg = "json_body=" in func

        if has_data_param and not (has_json_kwarg or has_json_body_kwarg):
            if "request_json(" in func:
                func = re.sub(
                    r"(query_params=query_params),?(\s*)",
                    rf"\1,\n                json_body={_BODY_DUMP},\2",
                    func,
                    count=1,
                )
            else:
                func = re.sub(
                    r"(params=query_params)(,?)(\s*\))",
                    rf"\1, json={_BODY_DUMP}\3",
                    func,
                )
        func = re.sub(r"\bdata\.dict\(\)", _BODY_DUMP, func)
        if not has_data_param and has_json_kwarg:
            func = re.sub(r",\s*json=data\.model_dump\([^)]*\)", "", func)
            func = re.sub(r"json=data\.model_dump\([^)]*\)", "", func)
        if not has_data_param and has_json_body_kwarg:
            func = re.sub(r",\s*json_body\s*=\s*data\.model_dump\([^)]*\)", "", func)
            func = re.sub(r"json_body\s*=\s*data\.model_dump\([^)]*\)\s*,?", "", func)
        fixed_funcs.append(func)
    return "".join(fixed_funcs)


_BASEMODEL_ATTRS = frozenset(
    name for name in dir(BaseModel) if not name.startswith("_")
)
_MODEL_FIELD = re.compile(
    r'^( +)(\w+)( *:[^\n=]+= *Field\(validation_alias="([^"]*)")', re.MULTILINE
)


def _fix_model_field_names(content: str) -> str:
    """Keeps each model field's wire name on the way out as well as in.

    The generator escapes a keyword field (`not` -> `not_`), and a field that
    shadows a BaseModel attribute is escaped here (`schema` -> `schema_`, or
    Pydantic warns on every `import kentik_api`). validation_alias alone
    reads the wire name but dumps the Python one, so a request sent
    `{"not_": true}` and the API ignored the negation. serialization_alias
    makes `model_dump(by_alias=True)` send `not` again.
    """

    def fix(m: re.Match[str]) -> str:
        indent, name, rest, wire = m[1], m[2], m[3], m[4]
        if name in _BASEMODEL_ATTRS:
            name += "_"
        if name != wire:
            rest += f', serialization_alias="{wire}"'
        return f"{indent}{name}{rest}"

    return _MODEL_FIELD.sub(fix, content)


def _fix_typing_wildcard(content: str) -> str:
    """Replaces `from typing import *` with an explicit import list."""
    if "from typing import *" not in content:
        return content
    return content.replace(
        "from typing import *",
        "from typing import Any, Callable, Dict, Generic, List, Optional, Set, Tuple, Type, TypeVar, Union",
    )


_TYPING_IMPORT = re.compile(r"^from typing import ([^\n(]+)$", re.MULTILINE)
_LOCAL_BINDING = re.compile(
    r"^(?:def|class)\s+(\w+)|^from \.+\w* import ([^\n(]+)", re.MULTILINE
)


def _alias_shadowed_typing_names(content: str) -> str:
    """Aliases each typing name the module also binds: `List` -> `TypingList`.

    An operation named `List` or a model named `Optional` would otherwise
    replace the typing name, and the next `List[...]` fails at import.
    """
    typing_import = _TYPING_IMPORT.search(content)
    if typing_import is None:
        return content
    imported = [name.strip() for name in typing_import.group(1).split(",")]
    bound: set[str] = set()
    for match in _LOCAL_BINDING.finditer(content):
        if match.group(1):
            bound.add(match.group(1))
        else:
            names = match.group(2).split("#")[0].split(",")
            bound |= {name.split(" as ")[-1].strip() for name in names}
    shadowed = sorted(set(imported) & bound)
    if not shadowed:
        return content
    if "Any" in shadowed:
        raise ValueError("A model or operation named `Any` shadows typing.Any")
    aliased = ", ".join(
        f"{name} as Typing{name}" if name in shadowed else name for name in imported
    )
    content = (
        content[: typing_import.start()]
        + f"from typing import {aliased}"
        + content[typing_import.end() :]
    )
    return re.sub(rf"(?<![.\w])({'|'.join(shadowed)})\[", r"Typing\1[", content)


def _make_models_import_transform(model_classes: set[str]) -> Callable[[str], str]:
    """Returns a transform that replaces wildcard model imports with explicit ones."""
    if not model_classes:
        return lambda content: content
    explicit_dotdot = f"from ..models import {', '.join(sorted(model_classes))}"
    explicit_local = f"from .models import {', '.join(sorted(model_classes))}"

    def _transform(content: str) -> str:
        content = content.replace(
            "from ..models import *", explicit_dotdot + "  # noqa: F401"
        )
        content = content.replace(
            "from .models import *", explicit_local + "  # noqa: F401"
        )
        return content

    return _transform


def _dedupe_top_level_function_names(content: str) -> str:
    """Renames duplicate top-level def names to avoid F811 collisions."""
    func_name_pattern = re.compile(
        r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", re.MULTILINE
    )
    seen: dict[str, int] = {}
    out: list[str] = []
    cursor = 0
    for match in func_name_pattern.finditer(content):
        func_name = match.group(1)
        seen[func_name] = seen.get(func_name, 0) + 1
        if seen[func_name] == 1:
            continue
        new_name = f"{func_name}_{seen[func_name]}"
        out.append(content[cursor : match.start(1)])
        out.append(new_name)
        cursor = match.end(1)
    if not out:
        return content
    out.append(content[cursor:])
    return "".join(out)


def _normalize_triple_quoted_docstrings(content: str) -> str:
    """Normalizes indentation of triple-quoted docstrings for docutils/Sphinx."""
    pattern = re.compile(r"(^[ \t]*)(\"\"\"|''')([\s\S]*?)(\2)", re.MULTILINE)

    def _rewrite(match: re.Match[str]) -> str:
        indent = match.group(1)
        quote = match.group(2)
        body = match.group(3)
        if "\n" not in body:
            return match.group(0)
        dedented = textwrap.dedent(body).replace("\r\n", "\n").strip("\n")
        if not dedented:
            return f"{indent}{quote}{quote}"
        lines = dedented.split("\n")
        inner_indent = indent + ("    " if indent else "")
        formatted_lines = [
            (f"{inner_indent}{line.strip()}" if line.strip() else "") for line in lines
        ]
        return f"{indent}{quote}\n" + "\n".join(formatted_lines) + f"\n{indent}{quote}"

    return pattern.sub(_rewrite, content)
