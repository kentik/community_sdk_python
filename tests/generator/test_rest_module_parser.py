# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Unit tests for scripts/generation/_shared.parse_generated_rest_module."""

from pathlib import Path

import pytest

from scripts.generation._shared import parse_generated_rest_module

_MINIMAL_OPERATION = """\
from typing import Optional
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from ..error import ListThingsError

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
"""

_KWONLY_PARAMS = """\
from typing import Optional
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from ..error import GetThingError

def GetThing(
    api_config_override: Optional[APIConfig] = None,
    *,
    thing_id: str,
    verbose: Optional[bool] = None,
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

_WRITE_OPERATION = """\
from typing import Optional
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from ..error import CreateThingError
from ..models import CreateThingRequest, CreateThingResponse

def CreateThing(
    api_config_override: Optional[APIConfig] = None,
    *,
    data: CreateThingRequest,
) -> CreateThingResponse:
    body = request_json(
        method="post",
        path="/things/v1/thing",
        api_config_override=api_config_override,
        expected_status=201,
        operation_name="CreateThing",
        error_cls=CreateThingError,
    )
    return CreateThingResponse(**body)
"""

_HELPER_NOT_AN_OP = """\
def _helper():
    return None
"""

_MULTI_OP = _MINIMAL_OPERATION + "\n" + _WRITE_OPERATION


def test_parses_minimal_get_operation(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_MINIMAL_OPERATION, encoding="utf-8")

    ops = parse_generated_rest_module(f)

    assert len(ops) == 1
    op = ops[0]
    assert op.name == "ListThings"
    assert op.http_method == "get"
    assert op.path == "/things/v1/thing"
    assert op.expected_status == 200
    assert op.operation_name == "ListThings"
    assert op.error_cls_name == "ListThingsError"
    assert op.return_type == "ListThingsResponse"


def test_positional_params_before_kwonly(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_KWONLY_PARAMS, encoding="utf-8")

    ops = parse_generated_rest_module(f)
    assert len(ops) == 1
    op = ops[0]

    assert op.kwonly_start == 1
    positional = op.params[: op.kwonly_start]
    kwonly = op.params[op.kwonly_start :]

    assert positional[0][0] == "api_config_override"
    assert kwonly[0] == ("thing_id", "str", True)  # required
    assert kwonly[1] == ("verbose", "Optional[bool]", False)  # optional


def test_f_string_path_is_reconstructed(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_KWONLY_PARAMS, encoding="utf-8")

    ops = parse_generated_rest_module(f)
    assert ops[0].path == "/things/v1/thing/{thing_id}"


def test_post_operation(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_WRITE_OPERATION, encoding="utf-8")

    ops = parse_generated_rest_module(f)
    assert ops[0].http_method == "post"
    assert ops[0].expected_status == 201
    kwonly = ops[0].params[ops[0].kwonly_start :]
    assert kwonly[0] == ("data", "CreateThingRequest", True)  # required kwonly


def test_helper_function_is_skipped(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_MINIMAL_OPERATION + _HELPER_NOT_AN_OP, encoding="utf-8")

    ops = parse_generated_rest_module(f)
    assert len(ops) == 1  # _helper is skipped; it has no request_json call


def test_multi_operation_file(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_MULTI_OP, encoding="utf-8")

    ops = parse_generated_rest_module(f)
    assert len(ops) == 2
    assert ops[0].name == "ListThings"
    assert ops[1].name == "CreateThing"


def test_empty_file_returns_empty_list(tmp_path: Path) -> None:
    f = tmp_path / "Empty.py"
    f.write_text("", encoding="utf-8")

    assert parse_generated_rest_module(f) == []


def test_nonexistent_file_returns_empty_list(tmp_path: Path) -> None:
    f = tmp_path / "nonexistent.py"
    assert parse_generated_rest_module(f) == []


def test_operation_is_frozen(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_MINIMAL_OPERATION, encoding="utf-8")

    op = parse_generated_rest_module(f)[0]
    with pytest.raises((AttributeError, TypeError)):
        op.name = "changed"  # ty: ignore[invalid-assignment]  # pyright: ignore[reportAttributeAccessIssue]


_QUERY_PARAMS = """\
from typing import Any, Dict, Optional
from kentik_api.core.api_config import APIConfig
from kentik_api.core.rest_runtime import request_json
from ..error import ListThingsError

def ListThings(
    api_config_override: Optional[APIConfig] = None,
    *,
    paginationlimit: Optional[int] = None,
    view: Optional[str] = None,
) -> ListThingsResponse:
    query_params: Dict[str, Any] = {
        "pagination.limit": paginationlimit,
        "view": view,
    }
    body = request_json(
        method="get",
        path="/things/v1/thing",
        api_config_override=api_config_override,
        query_params=query_params,
        expected_status=200,
        operation_name="ListThings",
        error_cls=ListThingsError,
    )
    return ListThingsResponse(**body)
"""


def test_query_params_map_wire_names_to_arguments(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_QUERY_PARAMS, encoding="utf-8")

    op = parse_generated_rest_module(f)[0]
    assert op.query_params == (
        ("pagination.limit", "paginationlimit"),
        ("view", "view"),
    )


def test_operation_without_query_params_has_none(tmp_path: Path) -> None:
    f = tmp_path / "ThingService.py"
    f.write_text(_KWONLY_PARAMS, encoding="utf-8")

    assert parse_generated_rest_module(f)[0].query_params == ()
