# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

from typing import ClassVar

import grpc
import pytest

from kentik_api.core.api_config import APIConfig
from kentik_api.core.grpc_runtime import (
    build_grpc_request,
    call_grpc,
    grpc_response_body,
    map_grpc_error,
)
from kentik_api.errors import (
    AuthenticationError,
    ConfigurationError,
    HTTPException,
    TransportError,
)

HTTP_MAPPED = {
    grpc.StatusCode.INVALID_ARGUMENT: 400,
    grpc.StatusCode.FAILED_PRECONDITION: 400,
    grpc.StatusCode.OUT_OF_RANGE: 400,
    grpc.StatusCode.PERMISSION_DENIED: 403,
    grpc.StatusCode.NOT_FOUND: 404,
    grpc.StatusCode.ALREADY_EXISTS: 409,
    grpc.StatusCode.ABORTED: 409,
    grpc.StatusCode.RESOURCE_EXHAUSTED: 429,
    grpc.StatusCode.UNKNOWN: 500,
    grpc.StatusCode.INTERNAL: 500,
    grpc.StatusCode.DATA_LOSS: 500,
    grpc.StatusCode.UNIMPLEMENTED: 501,
}
NO_RESPONSE = [
    grpc.StatusCode.CANCELLED,
    grpc.StatusCode.DEADLINE_EXCEEDED,
    grpc.StatusCode.UNAVAILABLE,
]


def test_classification_covers_every_non_ok_code():
    classified = set(HTTP_MAPPED) | set(NO_RESPONSE) | {grpc.StatusCode.UNAUTHENTICATED}

    assert classified == set(grpc.StatusCode) - {grpc.StatusCode.OK}
    assert len(classified) == 16


def test_unauthenticated_raises_auth_error(rpc_error):
    result = map_grpc_error(rpc_error(grpc.StatusCode.UNAUTHENTICATED, "bad token"))

    assert isinstance(result, AuthenticationError)
    assert "bad token" in str(result)


def test_google_rpc_status_details_reach_the_error(rpc_error):
    from google.protobuf.any_pb2 import Any as AnyMessage
    from google.rpc import error_details_pb2, status_pb2

    violation = error_details_pb2.BadRequest(
        field_violations=[{"field": "device.name", "description": "required"}]
    )
    known, unknown = AnyMessage(), AnyMessage(type_url="type.googleapis.com/x.Y")
    known.Pack(violation)
    status = status_pb2.Status(code=3, message="bad", details=[known, unknown])
    error = rpc_error(grpc.StatusCode.INVALID_ARGUMENT, "bad")
    error.trailing_metadata = lambda: [
        ("grpc-status-details-bin", status.SerializeToString())
    ]

    result = map_grpc_error(error)

    assert isinstance(result, HTTPException)
    assert result.details["rpc_status"] == {
        "code": 3,
        "message": "bad",
        "details": [
            {
                "@type": "type.googleapis.com/google.rpc.BadRequest",
                "fieldViolations": [
                    {"field": "device.name", "description": "required"}
                ],
            },
            {"@type": "type.googleapis.com/x.Y"},
        ],
    }
    assert result.details["rpc_status_code"] == 3


@pytest.mark.parametrize(
    "trailers",
    [None, [], [("grpc-status-details-bin", b"\xff\xff")]],
    ids=["none", "empty", "corrupt"],
)
def test_missing_or_corrupt_status_details_leave_details_empty(rpc_error, trailers):
    error = rpc_error(grpc.StatusCode.INVALID_ARGUMENT, "bad")
    error.trailing_metadata = lambda: trailers

    result = map_grpc_error(error)

    assert isinstance(result, HTTPException)
    assert result.details == {}


@pytest.mark.parametrize(
    ("code", "http_status"), HTTP_MAPPED.items(), ids=lambda v: str(v)
)
def test_api_faults_map_to_http_exception_keeping_the_grpc_code(
    rpc_error, code, http_status
):
    result = map_grpc_error(rpc_error(code, "fault"), method="gRPC", path="/svc/Op")

    assert type(result) is HTTPException
    assert result.status_code == http_status
    assert result.grpc_status_code == code.name
    assert (result.method, result.path) == ("gRPC", "/svc/Op")
    assert "fault" in str(result)


@pytest.mark.parametrize("code", NO_RESPONSE, ids=lambda c: c.name)
def test_no_response_codes_raise_transport_error_without_an_http_status(
    rpc_error, code
):
    result = map_grpc_error(rpc_error(code, "gone"), path="/svc/Op")

    assert type(result) is TransportError
    assert code.name in str(result)
    assert "/svc/Op" in str(result)


def test_unrecognized_code_raises_transport_error_naming_it(rpc_error):
    result = map_grpc_error(rpc_error("SOMETHING_NEW", "?"))

    assert type(result) is TransportError
    assert "SOMETHING_NEW" in str(result)


def test_details_none_guard(rpc_error):
    result = map_grpc_error(rpc_error(grpc.StatusCode.NOT_FOUND, None))

    assert isinstance(result, HTTPException)
    assert result.status_code == 404


def test_non_rpc_error_from_the_stub_is_not_reported_as_transport_failure():
    def _stub(_request):
        raise TypeError("bad request message")

    with pytest.raises(TypeError, match="bad request message"):
        call_grpc(_stub, object())


class _UnreadableLabelStub:
    """A stub whose method label cannot be read, raising a real RpcError."""

    def __init__(self, error: grpc.RpcError) -> None:
        self._error = error

    @property
    def _method(self):
        raise RuntimeError("label unavailable")

    def __call__(self, _request):
        raise self._error


def test_rpc_error_stays_the_cause_when_the_label_cannot_be_read(rpc_error):
    original = rpc_error(grpc.StatusCode.NOT_FOUND, "missing")
    stub = _UnreadableLabelStub(original)

    with pytest.raises(HTTPException) as exc_info:
        call_grpc(stub, object())

    assert exc_info.value.__cause__ is original


class _Stub:
    """Mimics a grpcio multicallable: callable, with a `_method` label."""

    def __init__(self, label, outcome) -> None:
        self._method = label
        self._outcome = outcome

    def __call__(self, request):
        if isinstance(self._outcome, BaseException):
            raise self._outcome
        return self._outcome(request)


def test_call_grpc_returns_the_stub_response_unchanged():
    request = object()

    response, rate_limit = call_grpc(
        _Stub(b"/svc.Service/Op", lambda r: ("reply", r)), request
    )

    assert response == ("reply", request)
    assert rate_limit is None


@pytest.mark.parametrize(
    "label", [b"/svc.Service/Op", "/svc.Service/Op"], ids=["bytes", "str"]
)
def test_call_grpc_labels_the_error_with_the_method_path(rpc_error, label):
    original = rpc_error(grpc.StatusCode.NOT_FOUND, "missing")

    with pytest.raises(HTTPException) as exc_info:
        call_grpc(_Stub(label, original), object())

    assert exc_info.value.path == "/svc.Service/Op"
    assert exc_info.value.method == "gRPC"
    assert exc_info.value.__cause__ is original


def test_call_grpc_labels_unknown_when_the_stub_has_no_label(rpc_error):
    def _stub(_request):
        raise rpc_error(grpc.StatusCode.NOT_FOUND, "missing")

    with pytest.raises(HTTPException) as exc_info:
        call_grpc(_stub, object())

    assert exc_info.value.path == "unknown"


@pytest.fixture
def device_pb2():
    import kentik_api.gen.pb_companions  # noqa: F401  # registers proto dependencies
    from kentik_api.gen.device.pb import device_pb2

    return device_pb2


def test_build_grpc_request_nests_dotted_field_paths(device_pb2):
    request = build_grpc_request(
        device_pb2.GetDeviceRequest,
        None,
        {"id": "42", "query.noCustomColumns": True},
    )

    assert request.id == "42"
    assert request.query.no_custom_columns is True


def test_build_grpc_request_merges_fields_into_the_body(device_pb2):
    request = build_grpc_request(
        device_pb2.UpdateDeviceRequest,
        {"device": {"deviceName": "edge-1"}},
        {"device.id": "42"},
    )

    assert request.device.id == "42"
    assert request.device.device_name == "edge-1"


def test_build_grpc_request_skips_unset_fields(device_pb2):
    request = build_grpc_request(
        device_pb2.GetDeviceRequest, None, {"id": "42", "query.noCustomColumns": None}
    )

    assert not request.HasField("query")


def test_build_grpc_request_rejects_a_field_the_request_does_not_declare(device_pb2):
    with pytest.raises(ConfigurationError):
        build_grpc_request(device_pb2.GetDeviceRequest, None, {"deviceid": "42"})


@pytest.mark.parametrize(
    ("body", "bad"),
    [
        ({"capability": {"dispalyName": "Edge"}}, "dispalyName"),
        ({"capability": {"name": "snmp", "nmae": "x"}}, "nmae"),
    ],
)
def test_build_grpc_request_rejects_an_unknown_body_key(capability_pb2, body, bad):
    with pytest.raises(ConfigurationError, match=bad):
        build_grpc_request(
            capability_pb2.UpdateCapabilityRequest,
            body,
            {"capability.name": "snmp"},
            update_mask_from="capability",
        )


def test_build_grpc_request_rejects_an_unknown_enum_name(device_pb2):
    with pytest.raises(ConfigurationError, match="DEVICE_VIEW_FUL"):
        build_grpc_request(
            device_pb2.ListDevicesRequest, {"view": "DEVICE_VIEW_FUL"}, {}
        )


@pytest.fixture
def capability_pb2():
    import kentik_api.gen.pb_companions  # noqa: F401  # registers proto dependencies
    from kentik_api.gen.kagent.pb import capability_pb2

    return capability_pb2


def test_patch_derives_update_mask_from_the_sent_keys(capability_pb2):
    request = build_grpc_request(
        capability_pb2.UpdateCapabilityRequest,
        {"capability": {"displayName": "Edge", "description": ""}},
        {"capability.name": "snmp"},
        update_mask_from="capability",
    )

    assert list(request.update_mask.paths) == ["display_name", "description"]
    assert request.capability.name == "snmp"


def test_update_mask_paths_recurse_into_nested_messages(device_pb2):
    from kentik_api.core.grpc_runtime import _mask_paths

    device = device_pb2.UpdateDeviceRequest().device
    sent = {"deviceName": "edge-1", "deviceSnmpV3Conf": {"username": "u"}}

    assert _mask_paths(device, sent) == ["device_name", "device_snmp_v3_conf.username"]


def test_no_update_mask_without_update_mask_from(capability_pb2):
    request = build_grpc_request(
        capability_pb2.UpdateCapabilityRequest,
        {"capability": {"displayName": "Edge"}},
        {"capability.name": "snmp"},
    )

    assert not request.update_mask.paths


def test_call_grpc_rejects_direct_per_call_config_override_for_grpc():
    called = False

    class _Stub:
        _method = "/svc.Service/Op"

        def __call__(self, _request, **_kwargs):
            nonlocal called
            called = True
            return b"ok"

    with pytest.raises(ConfigurationError, match="with_timeout"):
        call_grpc(
            _Stub(),
            object(),
            api_config=APIConfig(
                auth_email="override@example.com",
                auth_token="override-token",
                grpc_deadline=5.0,
            ),
        )

    assert not called


def test_call_grpc_allows_with_timeout_override_for_deadline_only():
    seen_timeout = None

    class _Stub:
        _method = "/svc.Service/Op"

        def __call__(self, _request, **kwargs):
            nonlocal seen_timeout
            seen_timeout = kwargs.get("timeout")
            return b"ok"

    base = APIConfig(auth_email="dev@example.com", auth_token="token")
    override = base.with_timeout(grpc_deadline=7.5)

    response, rate_limit = call_grpc(_Stub(), object(), api_config=override)

    assert response == b"ok"
    assert rate_limit is None
    assert seen_timeout == 7.5


def test_a_timeout_override_cannot_be_tampered_with():
    override = APIConfig(auth_email="dev@example.com", auth_token="token").with_timeout(
        grpc_deadline=7.5
    )

    with pytest.raises(AttributeError, match="read-only"):
        override.base_path = "https://127.0.0.1:1"


def test_call_grpc_raises_the_operation_error_class_like_rest(rpc_error):
    class ServiceError(HTTPException):
        pass

    class GetThingError(ServiceError):
        response_error_map: ClassVar[dict] = {}

    class GetThingNotFoundError(GetThingError):
        pass

    class GetThingUnexpectedError(GetThingError):
        pass

    GetThingError.response_error_map = {
        "404": GetThingNotFoundError,
        "default": GetThingUnexpectedError,
    }

    def failing(code):
        def stub(_request, **_kwargs):
            raise rpc_error(code, "boom")

        return stub

    with pytest.raises(GetThingNotFoundError) as exc_info:
        call_grpc(failing(grpc.StatusCode.NOT_FOUND), object(), error_cls=GetThingError)
    assert exc_info.value.status_code == 404
    assert exc_info.value.grpc_status_code == "NOT_FOUND"

    with pytest.raises(GetThingUnexpectedError):
        call_grpc(failing(grpc.StatusCode.INTERNAL), object(), error_cls=GetThingError)

    with pytest.raises(AuthenticationError):
        call_grpc(
            failing(grpc.StatusCode.UNAUTHENTICATED), object(), error_cls=GetThingError
        )
    with pytest.raises(TransportError):
        call_grpc(
            failing(grpc.StatusCode.UNAVAILABLE), object(), error_cls=GetThingError
        )


def test_empty_request_and_response_match_rest():
    """An RPC on google.protobuf.Empty sends `{}` and returns `{}`, as REST does."""
    from google.protobuf import empty_pb2

    request = build_grpc_request(empty_pb2.Empty, {}, {})

    assert isinstance(request, empty_pb2.Empty)
    assert grpc_response_body(empty_pb2.Empty()) == {}
