# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Unit tests for scripts/generation/fixup.py.

All tests use tmp_path. No schema download or full generation run is required.
"""

import ast
import textwrap
from pathlib import Path

import pytest

from scripts.generation._shared import normalize_symbol
from scripts.generation.fixup import (
    _alias_shadowed_typing_names,
    _cleanup_service_files,
    _dedupe_top_level_function_names,
    _fix_import_aliases,
    _fix_model_field_names,
    _fix_path_parameters,
    _fix_pydantic_construct,
    _fix_typing_wildcard,
    _fix_wildcard_exports,
    _inject_data_body,
    _make_models_import_transform,
    _normalize_triple_quoted_docstrings,
    _patch_service_files,
    _rebuild_models_init,
    fix_generated_service,
)


def test_rebuild_models_init_exports_all_classes(tmp_path):
    models = tmp_path / "models"
    models.mkdir()
    (models / "__init__.py").write_text("")
    (models / "Device.py").write_text("class Device:\n    pass\n")
    (models / "Interface.py").write_text("class Interface:\n    pass\n")

    _rebuild_models_init(tmp_path)

    init = (models / "__init__.py").read_text()
    assert "from .Device import Device as Device" in init
    assert "from .Interface import Interface as Interface" in init


def test_rebuild_models_init_skips_nonclass_files(tmp_path):
    models = tmp_path / "models"
    models.mkdir()
    (models / "__init__.py").write_text("")
    (models / "helpers.py").write_text("def helper(): pass\n")  # no class

    _rebuild_models_init(tmp_path)

    assert (models / "__init__.py").read_text() == ""


def test_rebuild_models_init_noop_without_models_dir(tmp_path):
    _rebuild_models_init(tmp_path)


def test_fix_wildcard_exports_replaces_star_import(tmp_path):
    (tmp_path / "foo.py").write_text("class Bar:\n    pass\n")
    init = tmp_path / "__init__.py"
    init.write_text("from .foo import *\n")

    _fix_wildcard_exports(tmp_path)

    assert "from .foo import Bar as Bar" in init.read_text()
    assert "import *" not in init.read_text()


def test_fix_wildcard_exports_skips_error_dirs(tmp_path):
    error_dir = tmp_path / "error"
    error_dir.mkdir()
    init = error_dir / "__init__.py"
    original = "from .foo import *\n"
    init.write_text(original)
    (error_dir / "foo.py").write_text("class Err:\n    pass\n")

    _fix_wildcard_exports(tmp_path)

    assert init.read_text() == original


def _make_service_dir(tmp_path: Path) -> Path:
    services = tmp_path / "services"
    services.mkdir(parents=True)
    return services


def test_patch_import_alias(tmp_path):
    svc = _make_service_dir(tmp_path)
    f = svc / "DeviceService.py"
    f.write_text("from ..api_config import APIConfig, HTTPException\ndef foo(): pass\n")

    _patch_service_files(tmp_path, set())

    content = f.read_text()
    assert "from kentik_api.core.api_config import APIConfig" in content
    assert "from kentik_api.errors import HTTPException" in content


def test_dedupe_function_names_renames_second_duplicate():
    content = textwrap.dedent("""\
        def List(a):
            pass

        def List(b):
            pass
        """)

    result = _dedupe_top_level_function_names(content)

    assert "def List(a):" in result
    assert "def List_2(b):" in result
    assert result.count("def List(") == 1


def test_dedupe_function_names_leaves_unique_names_unchanged():
    content = "def Foo():\n    pass\n\ndef Bar():\n    pass\n"
    assert _dedupe_top_level_function_names(content) == content


def test_normalize_docstrings_flattens_indentation():
    content = textwrap.dedent('''\
        class Foo:
            """
                Deeply indented.
                    More deeply.
            """
            pass
        ''')

    result = _normalize_triple_quoted_docstrings(content)

    lines = [
        ln
        for ln in result.splitlines()
        if ln.strip() in ("Deeply indented.", "More deeply.")
    ]
    assert len(lines) == 2
    assert lines[0].startswith(" " * 8)  # class body (4) + inner (4)
    assert lines[0].rstrip() == lines[1].rstrip().replace(
        "More deeply.", "Deeply indented."
    )


def test_normalize_docstrings_leaves_single_line_untouched():
    content = '    """Short docstring."""\n'
    assert _normalize_triple_quoted_docstrings(content) == content


def test_patch_typing_wildcard_import(tmp_path):
    svc = _make_service_dir(tmp_path)
    f = svc / "DeviceService.py"
    f.write_text("from typing import *\ndef foo(): pass\n")

    _patch_service_files(tmp_path, set())

    content = f.read_text()
    assert "from typing import *" not in content
    assert "from typing import" in content


def test_fix_generated_service_smoke(tmp_path):
    models = tmp_path / "models"
    models.mkdir()
    (models / "__init__.py").write_text("")
    (models / "Device.py").write_text("class Device:\n    pass\n")
    services = tmp_path / "services"
    services.mkdir()
    (services / "DeviceService.py").write_text(
        "from ..api_config import APIConfig, HTTPException\ndef foo(): pass\n"
    )

    fix_generated_service(tmp_path)

    assert "Device as Device" in (models / "__init__.py").read_text()
    assert (
        "from kentik_api.core.api_config import APIConfig"
        in (services / "DeviceService.py").read_text()
    )


@pytest.mark.parametrize("parent", ["pb", "error"])
def test_fix_generated_service_ignores_an_ancestor_named_pb_or_error(tmp_path, parent):
    service_dir = tmp_path / parent / "device"
    services = service_dir / "services"
    services.mkdir(parents=True)
    (services / "async_DeviceService.py").write_text("")
    (services / "DeviceService.py").write_text(
        "from ..api_config import APIConfig, HTTPException\ndef foo(): pass\n"
    )

    fix_generated_service(service_dir)

    assert not (services / "async_DeviceService.py").exists()
    assert (
        "from kentik_api.core.api_config import APIConfig"
        in (services / "DeviceService.py").read_text()
    )


def test_fix_import_aliases_combined():
    content = "from ..api_config import APIConfig, HTTPException\ndef foo(): pass\n"
    result = _fix_import_aliases(content)
    assert "from kentik_api.core.api_config import APIConfig" in result
    assert "from kentik_api.errors import HTTPException" in result


def test_fix_import_aliases_as_alias():
    result = _fix_import_aliases("from ..api_config import APIConfig as APIConfig\n")
    assert result == "from kentik_api.core.api_config import APIConfig\n"


def test_fix_pydantic_construct_rewrites_model_instantiation():
    content = "return Foo(**body) if body else Foo()\n"
    result = _fix_pydantic_construct(content)
    assert "model_construct" in result
    assert "body is not None" in result


def test_fix_path_parameters_encodes_each_placeholder():
    result = _fix_path_parameters(
        "from kentik_api.core.rest_runtime import request_json\n"
        "path=f'/v1/device/{device.id}/{tagId}'"
    )
    assert result == (
        "from kentik_api.core.rest_runtime import path_segment\n"
        "from kentik_api.core.rest_runtime import request_json\n"
        "path=f'/v1/device/{path_segment(deviceid)}/{path_segment(tagId)}'"
    )


def test_fix_path_parameters_names_keyword_placeholders_as_their_argument():
    result = _fix_path_parameters(
        "from kentik_api.core.rest_runtime import request_json\n"
        "path=f'/v1/range/{from}/{class.id}'"
    )
    assert "path=f'/v1/range/{path_segment(from_)}/{path_segment(classid)}'" in result


@pytest.mark.parametrize(
    "name",
    ["id", "device.id", "from", "class.id", "device-id", "2fa", "Get-Thing", "café"],
)
def test_normalize_symbol_matches_the_rest_generator(name):
    from openapi_python_generator.language_converters.python import common

    assert normalize_symbol(name) == common.normalize_symbol(name)


def test_fix_path_parameters_leaves_a_module_without_placeholders_alone():
    content = (
        "from kentik_api.core.rest_runtime import request_json\npath=f'/v1/devices'"
    )
    assert _fix_path_parameters(content) == content


def test_fix_path_parameters_requires_the_request_json_import():
    with pytest.raises(ValueError, match="request_json"):
        _fix_path_parameters("path=f'/v1/device/{id}'")


def test_fix_model_field_names_escapes_basemodel_attributes():
    content = (
        '    schema : Optional[MetricsSchema] = Field(validation_alias="schema" , default = None )\n'
        '    name : str = Field(validation_alias="name" )\n'
    )

    assert _fix_model_field_names(content) == (
        '    schema_ : Optional[MetricsSchema] = Field(validation_alias="schema", '
        'serialization_alias="schema" , default = None )\n'
        '    name : str = Field(validation_alias="name" )\n'
    )


def test_fix_model_field_names_dumps_an_escaped_keyword_under_its_wire_name():
    content = (
        '    not_ : Optional[bool] = Field(validation_alias="not" , default = None )\n'
    )

    assert _fix_model_field_names(content) == (
        '    not_ : Optional[bool] = Field(validation_alias="not", '
        'serialization_alias="not" , default = None )\n'
    )


def test_fix_typing_wildcard_replaces_star():
    result = _fix_typing_wildcard("from typing import *\nx = 1\n")
    assert "from typing import *" not in result
    assert "Optional" in result


def test_fix_typing_wildcard_noop_without_star():
    content = "from typing import Optional\n"
    assert _fix_typing_wildcard(content) == content


def test_operation_named_list_aliases_typing_list():
    content = "from typing import Optional, List\n\ndef List(x: List[str]) -> str:\n    pass\n"
    result = _alias_shadowed_typing_names(content)
    assert result.startswith("from typing import Optional, List as TypingList\n")
    assert "def List(x: TypingList[str])" in result


@pytest.mark.parametrize(
    ("name", "args"), [("Optional", "str"), ("Set", "str"), ("Dict", "str, int")]
)
def test_imported_model_named_like_a_typing_name_is_aliased(name, args):
    content = (
        f"from typing import Dict, Optional, Set\n"
        f"from ..models import Device, {name}  # noqa: F401\n\n"
        f"def Get(x: {name}[{args}], m: {name}) -> Device:\n    pass\n"
    )
    result = _alias_shadowed_typing_names(content)

    namespace: dict = {name: type(name, (), {}), "Device": object}
    exec(compile(result.replace("from ..models", "# "), "m", "exec"), namespace)  # noqa: S102 - runs the patched source under test
    assert f"def Get(x: Typing{name}[{args}], m: {name})" in result


def test_model_named_any_fails_generation():
    content = "from typing import Any\nfrom .Any import Any\n"
    with pytest.raises(ValueError, match="Any"):
        _alias_shadowed_typing_names(content)


def test_alias_shadowed_typing_names_noop_without_a_collision():
    content = "from typing import List\n\ndef Foo() -> List[str]:\n    pass\n"
    assert _alias_shadowed_typing_names(content) == content


def test_make_models_import_transform_replaces_wildcard():
    transform = _make_models_import_transform({"DeviceResponse", "DeviceRequest"})
    content = "from ..models import *\n"
    result = transform(content)
    assert "DeviceRequest" in result
    assert "DeviceResponse" in result
    assert "import *" not in result


def test_make_models_import_transform_noop_when_empty():
    transform = _make_models_import_transform(set())
    content = "from ..models import *\n"
    assert transform(content) == content


def test_cleanup_service_files_deletes_async_files(tmp_path):
    svc = tmp_path / "services"
    svc.mkdir()
    async_file = svc / "async_DeviceService.py"
    async_file.write_text("# async")
    keep = svc / "DeviceService.py"
    keep.write_text("# keep")

    _cleanup_service_files(tmp_path)

    assert not async_file.exists()
    assert keep.exists()


def test_cleanup_service_files_renames_service_service(tmp_path):
    svc = tmp_path / "services"
    svc.mkdir()
    bad = svc / "DeviceService_service.py"
    bad.write_text("# service")

    _cleanup_service_files(tmp_path)

    assert not bad.exists()
    assert (svc / "DeviceService.py").exists()


def test_inject_data_body_adds_json_body_param():
    content = textwrap.dedent("""\
        def CreateDevice(api_config_override=None, *, data: CreateDeviceRequest) -> CreateDeviceResponse:
            query_params = {}
            body = request_json(
                method="post",
                path="/device",
                api_config_override=api_config_override,
                query_params=query_params,
                expected_status=201,
            )
        """)
    result = _inject_data_body(content)
    assert "json_body=data.model_dump(by_alias=True, exclude_unset=True)" in result
    ast.parse(result)


@pytest.mark.parametrize("last", [True, False])
def test_inject_data_body_output_parses_wherever_query_params_sits(last):
    tail = "" if last else "\n        expected_status=201,"
    content = (
        "def Create(*, data: Req) -> Resp:\n"
        "    body = request_json(\n"
        f"        query_params=query_params{'' if last else ','}{tail}\n"
        "    )\n"
    )
    result = _inject_data_body(content)

    ast.parse(result)
    assert "json_body=data.model_dump" in result


def test_inject_data_body_ignores_a_parameter_ending_in_data():
    content = textwrap.dedent("""\
        def ListDevices(*, includeMetadata: bool) -> Resp:
            body = request_json(
                query_params=query_params,
                expected_status=200,
            )
        """)

    assert _inject_data_body(content) == content
