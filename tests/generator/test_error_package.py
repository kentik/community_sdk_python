# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.generation.error_package import (
    OperationErrorMetadata,
    collect_operation_error_responses,
    error_class_base,
    generate_service_error_package,
    inject_service_error_handling,
    merge_operation_error_responses,
    service_error_class_name,
    service_error_response_class_name,
)


def test_service_error_class_name():
    assert service_error_class_name("ListDevices") == "ListDevicesError"


def test_service_error_response_class_name_known_status():
    assert (
        service_error_response_class_name("ListDevices", "404")
        == "ListDevicesNotFoundError"
    )


def test_service_error_response_class_name_unknown_status_falls_back_to_http_prefix():
    assert (
        service_error_response_class_name("ListDevices", "418")
        == "ListDevicesHttp418Error"
    )


@pytest.mark.parametrize(
    ("method", "expected"),
    [
        ("list_devices", "ListDevices"),
        ("auto_ack_list", "AutoAckList"),
        ("get_event_by_ctime", "GetEventByCtime"),
        ("import_", "DeviceImport"),
    ],
)
def test_error_class_base_follows_the_client_method(method, expected):
    assert error_class_base(method, "Device") == expected


def _write_swagger(tmp_path: Path, name: str, paths: dict) -> Path:
    swagger_path = tmp_path / name
    swagger_path.write_text(json.dumps({"paths": paths}), encoding="utf-8")
    return swagger_path


def test_collect_operation_error_responses_ignores_2xx(tmp_path: Path):
    swagger_path = _write_swagger(
        tmp_path,
        "device.swagger.json",
        {
            "/devices/v1/list": {
                "get": {
                    "operationId": "ListDevices",
                    "responses": {
                        "200": {"description": "ok"},
                        "404": {"description": "not found"},
                    },
                }
            }
        },
    )

    errors = collect_operation_error_responses(swagger_path)

    assert set(errors) == {"GET /devices/<version>/list"}
    assert set(errors["GET /devices/<version>/list"]["responses"]) == {"404"}


def test_collect_operation_error_responses_keeps_operations_without_errors(
    tmp_path: Path,
):
    swagger_path = _write_swagger(
        tmp_path,
        "device.swagger.json",
        {"/devices": {"get": {"operationId": "ListDevices", "responses": {"200": {}}}}},
    )

    assert (
        collect_operation_error_responses(swagger_path)["GET /devices"]["responses"]
        == {}
    )


def test_merge_operation_error_responses_combines_responses_across_files():
    first: dict[str, OperationErrorMetadata] = {
        "GET /devices": {
            "path": "/devices",
            "method": "GET",
            "responses": {"404": {"description": "not found", "schema_ref": None}},
        }
    }
    second: dict[str, OperationErrorMetadata] = {
        "GET /devices": {
            "path": "/devices",
            "method": "GET",
            "responses": {"500": {"description": "boom", "schema_ref": None}},
        }
    }

    merged = merge_operation_error_responses([first, second])

    assert set(merged["GET /devices"]["responses"]) == {"404", "500"}


def _rest_function(name: str, path: str) -> str:
    return (
        f"def {name}(api_config_override=None):\n"
        "    return request_json(\n"
        '        method="get",\n'
        f'        path="{path}",\n'
        "        api_config_override=api_config_override,\n"
        "        expected_status=200,\n"
        f'        operation_name="{name}",\n'
        f"        error_cls={name}Error,\n"
        "    )\n\n\n"
    )


def _service(
    tmp_path: Path, modules: dict[str, dict[str, tuple[str, str]]]
) -> tuple[Path, dict[tuple[Path, str], str], dict[str, OperationErrorMetadata]]:
    """A Service with REST modules of `function: (client method, path)`, each with a 404."""
    service_dir = tmp_path / "device"
    (service_dir / "services").mkdir(parents=True)
    method_names: dict[tuple[Path, str], str] = {}
    paths: dict = {}
    for module, functions in modules.items():
        rest_file = service_dir / "services" / f"{module}.py"
        rest_file.write_text(
            "from kentik_api.core.rest_runtime import request_json\n"
            "# __ERROR_IMPORTS_PLACEHOLDER__\n\n\n"
            + "".join(
                _rest_function(name, path) for name, (_, path) in functions.items()
            ),
            encoding="utf-8",
        )
        for name, (method, path) in functions.items():
            method_names[(rest_file, name)] = method
            paths[path] = {
                "get": {
                    "operationId": name,
                    "responses": {"404": {"description": "not found"}},
                }
            }
    swagger_path = _write_swagger(tmp_path, "device.swagger.json", paths)
    return service_dir, method_names, collect_operation_error_responses(swagger_path)


def _error_namespace(service_dir: Path) -> dict:
    namespace: dict = {"__name__": "generated_error"}
    source = (service_dir / "error" / "__init__.py").read_text(encoding="utf-8")
    exec(compile(source, "generated_error", "exec"), namespace)  # noqa: S102 - runs the generated module under test
    return namespace


def test_error_classes_are_named_after_the_client_method(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path, {"DeviceService": {"ListDevices": ("list_devices", "/devices")}}
    )

    generate_service_error_package(service_dir, errors, method_names)

    namespace = _error_namespace(service_dir)
    assert issubclass(namespace["ListDevicesError"], namespace["DeviceError"])
    assert issubclass(
        namespace["ListDevicesNotFoundError"], namespace["ListDevicesError"]
    )
    assert namespace["ERROR_BY_METHOD"] == {
        "list_devices": namespace["ListDevicesError"]
    }


def test_a_renamed_operation_id_keeps_the_error_class(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path, {"DeviceService": {"DevicesList": ("list_devices", "/devices")}}
    )

    generate_service_error_package(service_dir, errors, method_names)

    rest = (service_dir / "services" / "DeviceService.py").read_text()
    assert "from ..error import ListDevicesError" in rest
    assert "error_cls=ListDevicesError," in rest
    assert "DevicesListError" not in rest
    assert "ListDevicesError" in _error_namespace(service_dir)


def test_a_shared_operation_id_gets_one_error_class_per_method(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path,
        {
            "AlertService": {"List": ("alert_list", "/alerts")},
            "AlertAutoAckService": {"List": ("auto_ack_list", "/auto-acks")},
        },
    )

    generate_service_error_package(service_dir, errors, method_names)

    services = service_dir / "services"
    assert "error_cls=AlertListError," in (services / "AlertService.py").read_text()
    assert (
        "error_cls=AutoAckListError,"
        in (services / "AlertAutoAckService.py").read_text()
    )
    namespace = _error_namespace(service_dir)
    assert {"AlertListError", "AutoAckListError"} <= set(namespace["__all__"])


def test_a_raised_response_error_is_caught_by_its_operation_class(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path, {"DeviceService": {"ListDevices": ("list_devices", "/devices")}}
    )
    generate_service_error_package(service_dir, errors, method_names)
    namespace = _error_namespace(service_dir)

    response = type(
        "Response",
        (),
        {"status_code": 404, "text": "", "headers": {}, "json": lambda self: {}},
    )()
    error = namespace["ListDevicesError"].from_response(
        response, operation_name="ListDevices", method="GET", path="/devices"
    )

    assert type(error) is namespace["ListDevicesNotFoundError"]
    assert isinstance(error, namespace["DeviceError"])


def test_response_description_is_kept_verbatim_in_the_docstring(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path, {"DeviceService": {"ListDevices": ("list_devices", "/devices")}}
    )
    description = 'Bad \\u00zz path C:\\bin, """quoted"""\nsecond line'
    errors["GET /devices"]["responses"]["404"]["description"] = description

    generate_service_error_package(service_dir, errors, method_names)

    doc = _error_namespace(service_dir)["ListDevicesNotFoundError"].__doc__
    assert 'Bad \\u00zz path C:\\bin, """quoted""" second line' in doc


def test_swagger_and_rest_operations_that_differ_fail(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path, {"DeviceService": {"ListDevices": ("list_devices", "/devices")}}
    )
    errors["GET /other"] = errors["GET /devices"]

    with pytest.raises(ValueError, match="GET /other"):
        generate_service_error_package(service_dir, errors, method_names)


def test_error_class_names_that_collide_fail(tmp_path: Path):
    service_dir, method_names, errors = _service(
        tmp_path,
        {
            "DeviceService": {
                "List": ("list", "/a"),
                "ListNotFound": ("list_not_found", "/b"),
            }
        },
    )

    with pytest.raises(ValueError, match="ListNotFoundError"):
        generate_service_error_package(service_dir, errors, method_names)


_REST_MODULE = (
    "from kentik_api.core.rest_runtime import request_json\n"
    "# __ERROR_IMPORTS_PLACEHOLDER__\n"
    "\n"
    "def ListDevices(api_config_override=None):\n"
    "    return request_json(\n"
    "        operation_name='ListDevices',\n"
    "        error_cls=ListDevicesError,\n"
    "    )\n"
)


def test_inject_service_error_handling_adds_import_via_sentinel():
    result = inject_service_error_handling(_REST_MODULE, {"ListDevices": "XError"})

    assert "from ..error import XError" in result
    assert "error_cls=XError," in result
    assert "# __ERROR_IMPORTS_PLACEHOLDER__" not in result


def test_inject_service_error_handling_adds_import_via_legacy_anchor():
    content = _REST_MODULE.replace("# __ERROR_IMPORTS_PLACEHOLDER__\n", "")

    result = inject_service_error_handling(content, {"ListDevices": "XError"})

    assert "from ..error import XError" in result


def test_inject_service_error_handling_removes_placeholder_when_no_operations():
    content = (
        "from kentik_api.core.rest_runtime import request_json\n"
        "# __ERROR_IMPORTS_PLACEHOLDER__\n"
        "\n"
        "def helper():\n"
        "    return 1\n"
    )

    result = inject_service_error_handling(content, {})

    assert "# __ERROR_IMPORTS_PLACEHOLDER__" not in result


def test_inject_silent_when_no_operations_and_no_anchor():
    content = "def helper():\n    return 42\n"

    assert inject_service_error_handling(content, {}) == content


def test_inject_raises_when_anchor_missing():
    content = (
        "def Foo(api_config_override=None):\n    return other(error_cls=FooError)\n"
    )

    with pytest.raises(ValueError, match="rest_runtime|PLACEHOLDER"):
        inject_service_error_handling(content, {"Foo": "FooError"})
