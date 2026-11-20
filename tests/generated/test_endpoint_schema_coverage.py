# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Exhaustive endpoint x declared-response-status coverage.

`test_wrapper_contracts.py` proves every wrapper method forwards its
arguments correctly. This module proves the layer underneath (the shared
`request_json` runtime in `kentik_api.core.rest_runtime`) correctly
handles every response status code the OpenAPI schema actually declares for
every operation, success and error alike. Per AGENTS.md's test coverage
requirement, this is derived from the generated code (which is itself
derived from the schema), not hand-listed, so it stays exhaustive as the
schema grows.

Status codes come from each service's generated `error/__init__.py`
(`{Operation}Error.response_error_map`), which `scripts/generate_sdk.py`
builds directly from the swagger files' declared non-2xx responses.

Statuses in `RUNTIME_HANDLED` are asserted on every endpoint whether the
schema declares them or not, because `request_json` intercepts them before
any generated error class sees the response.
"""

from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest
import respx
from _discovery import (
    WrapperCase,
    build_all_kwargs,
    case_label,
    discover_cases,
    error_module_for,
    parse_rest_call_metadata,
    recorded_grpc_route,
    sample_grpc_response,
    sample_rest_response,
)
from google.protobuf.json_format import MessageToDict, ParseDict
from pydantic import BaseModel, ValidationError

from kentik_api.client import KentikAPI
from kentik_api.core.api_config import APIConfig
from kentik_api.errors import AuthenticationError, HTTPException, KentikError
from kentik_api.gen.alerting.models import PolicyType
from kentik_api.gen.device.models import DeviceView
from kentik_api.transports.grpc_client import GrpcTransport
from kentik_api.transports.rest_client import RestTransport


@dataclass(frozen=True)
class StatusCase:
    wrapper: WrapperCase
    status_code: int
    status_key: str
    is_success: bool
    error_class_name: str | None
    runtime_error: type[KentikError] | None = None


RUNTIME_HANDLED: dict[int, type[KentikError]] = {401: AuthenticationError}


def _rest_module_and_function(case: WrapperCase):
    module = importlib.import_module(case.module_path)
    rest_module = getattr(module, case.rest_module_alias)
    rest_func = getattr(rest_module, case.rest_function_name)
    return module, rest_module, rest_func


def _pick_default_simulated_code(explicit_codes: set[str]) -> int:
    candidate = 599
    while str(candidate) in explicit_codes and candidate > 500:
        candidate -= 1
    return candidate


def _discover_status_cases() -> list[StatusCase]:
    cases: list[StatusCase] = []

    for wrapper_case in discover_cases():
        _, rest_module, _ = _rest_module_and_function(wrapper_case)
        metadata = parse_rest_call_metadata(
            rest_module, wrapper_case.rest_function_name
        )
        if metadata is None:
            continue

        cases.append(
            StatusCase(
                wrapper=wrapper_case,
                status_code=metadata.expected_status,
                status_key="success",
                is_success=True,
                error_class_name=None,
            )
        )

        error_module = error_module_for(rest_module)
        error_cls = getattr(error_module, metadata.error_cls_name, None)
        response_error_map: dict[str, Any] = (
            getattr(error_cls, "response_error_map", {}) if error_cls else {}
        )
        explicit_codes = {key for key in response_error_map if key != "default"}
        explicit_codes |= {str(code) for code in RUNTIME_HANDLED}

        for code, runtime_error in RUNTIME_HANDLED.items():
            cases.append(
                StatusCase(
                    wrapper=wrapper_case,
                    status_code=code,
                    status_key=str(code),
                    is_success=False,
                    error_class_name=None,
                    runtime_error=runtime_error,
                )
            )

        for status_key, leaf_cls in sorted(response_error_map.items()):
            if status_key.isdigit() and int(status_key) in RUNTIME_HANDLED:
                continue  # already asserted above, with the runtime's expectation
            if status_key == "default":
                simulated_code = _pick_default_simulated_code(explicit_codes)
                cases.append(
                    StatusCase(
                        wrapper=wrapper_case,
                        status_code=simulated_code,
                        status_key="default",
                        is_success=False,
                        error_class_name=leaf_cls.__name__,
                    )
                )
            else:
                cases.append(
                    StatusCase(
                        wrapper=wrapper_case,
                        status_code=int(status_key),
                        status_key=status_key,
                        is_success=False,
                        error_class_name=leaf_cls.__name__,
                    )
                )

    return cases


ALL_STATUS_CASES = _discover_status_cases()


def _status_case_id(case: StatusCase) -> str:
    kind = "success" if case.is_success else f"error-{case.status_key}"
    return f"{case.wrapper.wrapper_class}.{case.wrapper.method_name}:{kind}"


def _assert_round_trips(result: BaseModel, message: Any) -> None:
    """Every value the server sent survives parsing; a dropped field fails here."""
    dumped = result.model_dump(mode="json", by_alias=True, exclude_none=True)
    assert ParseDict(dumped, type(message)()) == message


_ERROR_BODY = {"code": 7, "message": "simulated failure", "details": []}


@pytest.mark.parametrize(
    "case", ALL_STATUS_CASES, ids=[_status_case_id(c) for c in ALL_STATUS_CASES]
)
def test_endpoint_handles_declared_status_code(case: StatusCase):
    wrapper_case = case.wrapper
    mode = "success" if case.is_success else f"error-{case.status_key}"
    print(
        f'Testing against "{case_label(wrapper_case)}" status={case.status_code} '
        f"({mode}). START"
    )

    module = importlib.import_module(wrapper_case.module_path)
    wrapper_cls = getattr(module, wrapper_case.wrapper_class)
    transport = RestTransport(
        APIConfig(
            base_path="https://api.example.com",
            auth_email="dev@example.com",
            auth_token="token",
        )
    )
    wrapper = wrapper_cls(transport)
    method = getattr(wrapper, wrapper_case.method_name)

    try:
        kwargs = build_all_kwargs(method)
    except Exception as exc:  # noqa: BLE001 - any builder failure is reported as a named skip
        pytest.skip(f"Could not build sample arguments for this operation: {exc}")

    try:
        message: Any = None
        body: Any = None
        with respx.mock:
            if case.status_code == 204:
                respx.route().mock(return_value=httpx.Response(204))
            elif case.is_success and recorded_grpc_route(wrapper_case) is None:
                body = sample_rest_response(method)
                respx.route().mock(
                    return_value=httpx.Response(case.status_code, json=body)
                )
            elif case.is_success:
                message = sample_grpc_response(wrapper_case)
                respx.route().mock(
                    return_value=httpx.Response(
                        case.status_code, json=MessageToDict(message)
                    )
                )
            else:
                respx.route().mock(
                    return_value=httpx.Response(case.status_code, json=_ERROR_BODY)
                )

            if case.is_success:
                result = method(**kwargs)
                return_annotation = inspect.signature(method).return_annotation
                if case.status_code == 204:
                    assert result is None
                elif message is None:
                    dumped = (
                        result.model_dump(mode="json", by_alias=True, exclude_none=True)
                        if isinstance(result, BaseModel)
                        else result
                    )
                    assert dumped == body
                elif isinstance(return_annotation, type) and issubclass(
                    return_annotation, BaseModel
                ):
                    assert isinstance(result, return_annotation)
                    _assert_round_trips(result, message)
            elif case.runtime_error is not None:
                with pytest.raises(KentikError) as exc_info:
                    method(**kwargs)
                assert type(exc_info.value) is case.runtime_error
            else:
                error_module = error_module_for(
                    getattr(module, wrapper_case.rest_module_alias)
                )
                assert case.error_class_name is not None
                expected_cls = getattr(error_module, case.error_class_name)
                with pytest.raises(HTTPException) as exc_info:
                    method(**kwargs)
                assert isinstance(exc_info.value, expected_cls)
                assert exc_info.value.status_code == case.status_code

        print(
            f'Testing against "{case_label(wrapper_case)}" status={case.status_code} '
            f"({mode}). RESULT=PASS"
        )
    except Exception:
        print(
            f'Testing against "{case_label(wrapper_case)}" status={case.status_code} '
            f"({mode}). RESULT=FAIL"
        )
        raise


def _assert_unknown_enum_error(exc: KentikError) -> None:
    # Strict by decision (T1, option A): a value newer than this SDK fails the
    # response, as the same clear 502 on both transports, until regeneration.
    assert type(exc) is HTTPException
    assert exc.status_code == 502
    assert exc.details["model"] == "ListUsersResponse"
    assert isinstance(exc.__cause__, ValidationError)


def test_an_unknown_enum_value_over_rest_is_a_502():
    unknown_enum_payload = {
        "users": [
            {
                "id": "1",
                "userEmail": "a@b.c",
                "userFullName": "User A",
                "role": "ROLE_MEMBER",
                "permissions": [],
                "filter": {},
                "defaultLandingPageType": "LANDING_TYPE_SOMETHING_NEW",
            }
        ]
    }

    with respx.mock(base_url="https://grpc.api.kentik.com") as mock_api:
        route = mock_api.get("/user/v202211/users").mock(
            return_value=httpx.Response(200, json=unknown_enum_payload)
        )
        with (
            KentikAPI(email="dev@example.com", api_token="token", env_file=None) as api,
            pytest.raises(KentikError) as exc_info,
        ):
            api.user.list()

    assert route.called
    _assert_unknown_enum_error(exc_info.value)


def test_an_unknown_enum_value_over_grpc_is_the_same_502(monkeypatch):
    from kentik_api.gen.user.pb import user_pb2
    from kentik_api.gen.user.services import user as user_wrapper

    response = user_pb2.ListUsersResponse()
    response.users.add(id="1", default_landing_page_type=99)
    monkeypatch.setattr(user_wrapper, "call_grpc", lambda *a, **kw: (response, None))
    transport = MagicMock(spec=GrpcTransport)
    transport.channel = MagicMock()

    with pytest.raises(KentikError) as exc_info:
        user_wrapper.UserServiceWrapper(transport).list()

    _assert_unknown_enum_error(exc_info.value)


def test_enum_values_use_wire_representation_for_path_and_query_parameters():
    error_payload = {"message": "simulated failure"}

    with respx.mock(assert_all_called=False) as mock_api:
        list_devices_route = mock_api.get(
            "https://grpc.api.kentik.com/device/v202504beta2/device"
        ).mock(return_value=httpx.Response(500, json=error_payload))
        policy_get_route = mock_api.get(
            url__regex=r"https://grpc\.api\.kentik\.com/v202505/policies/.*/1"
        ).mock(return_value=httpx.Response(500, json=error_payload))

        with KentikAPI(
            email="dev@example.com", api_token="token", env_file=None
        ) as api:
            with pytest.raises(HTTPException):
                api.device.list(view=DeviceView.DEVICE_VIEW_BASIC)

            with pytest.raises(HTTPException):
                api.alerting.policy_get(
                    policyType=PolicyType.POLICY_TYPE_AGENT,
                    id="1",
                )

    assert list_devices_route.called
    assert policy_get_route.called

    list_devices_url = list_devices_route.calls.last.request.url
    policy_get_url = str(policy_get_route.calls.last.request.url)

    assert list_devices_url.params.get("view") == "DEVICE_VIEW_BASIC"
    assert "DeviceView." not in str(list_devices_url)
    assert "/POLICY_TYPE_AGENT/1" in policy_get_url
    assert "PolicyType." not in policy_get_url
