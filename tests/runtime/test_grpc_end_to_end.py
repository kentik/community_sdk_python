# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""A generated wrapper call over a real gRPC channel to an in-process server (T2)."""

from __future__ import annotations

from concurrent import futures

import grpc
import pytest

from kentik_api.core.api_config import APIConfig
from kentik_api.gen.device.error import GetUnexpectedError
from kentik_api.gen.device.pb import device_pb2, device_pb2_grpc
from kentik_api.gen.device.services.device import DeviceServiceWrapper
from kentik_api.transports.grpc_client import GrpcTransport

_DEADLINE_SECONDS = 7.5
_SERVER_CLOCK_TOLERANCE_SECONDS = 0.01


class _DeviceService(device_pb2_grpc.DeviceServiceServicer):
    def __init__(self) -> None:
        self.seen: dict = {}

    def GetDevice(self, request, context):
        self.seen = {
            "id": request.id,
            "metadata": dict(context.invocation_metadata()),
            "time_remaining": context.time_remaining(),
        }
        if request.id == "missing":
            context.abort(grpc.StatusCode.NOT_FOUND, "no such device")
        return device_pb2.GetDeviceResponse(
            device=device_pb2.DeviceDetailed(
                id=request.id,
                device_name="edge-1",
                labels=[device_pb2.Label(id="7", name="core")],
            )
        )


@pytest.fixture
def served(monkeypatch):
    """Yields (servicer, wrapper) with the transport's real auth plugin on the wire.

    gRPC only sends call credentials over a secure channel, so the transport's
    TLS credentials become local credentials, which count as secure on loopback.
    """
    servicer = _DeviceService()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    device_pb2_grpc.add_DeviceServiceServicer_to_server(servicer, server)
    port = server.add_secure_port("localhost:0", grpc.local_server_credentials())
    server.start()
    monkeypatch.setattr(grpc, "ssl_channel_credentials", grpc.local_channel_credentials)
    transport = GrpcTransport(
        APIConfig(
            auth_email="dev@example.com",
            auth_token="token",
            grpc_deadline=_DEADLINE_SECONDS,
        ),
        target=f"localhost:{port}",
    )
    try:
        yield servicer, DeviceServiceWrapper(transport)
    finally:
        transport.close()
        server.stop(0)


def test_a_wrapper_call_sends_auth_a_deadline_and_the_path_argument(served):
    servicer, device = served

    device.get(deviceid="42")

    assert servicer.seen["id"] == "42"
    assert servicer.seen["metadata"]["x-ch-auth-email"] == "dev@example.com"
    assert servicer.seen["metadata"]["x-ch-auth-api-token"] == "token"
    assert (
        0
        < servicer.seen["time_remaining"]
        <= (_DEADLINE_SECONDS + _SERVER_CLOCK_TOLERANCE_SECONDS)
    )


def test_a_populated_response_parses_into_the_rest_model(served):
    _, device = served

    response = device.get(deviceid="42")

    assert response.device is not None
    assert response.device.id == "42"
    assert response.device.deviceName == "edge-1"
    assert response.device.labels is not None
    label = response.device.labels[0]
    assert label is not None
    assert (label.id, label.name) == ("7", "core")


def test_a_server_error_raises_the_operations_error_class(served):
    _, device = served

    with pytest.raises(GetUnexpectedError) as exc_info:
        device.get(deviceid="missing")

    assert exc_info.value.status_code == 404
