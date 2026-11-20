# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Verifies each gRPC wrapper call reaches the right RPC with every argument set.

Mocked forwarding tests cannot see either failure this file guards against:
a call routed to another proto service's RPC of the same name (alerting's
AlertAutoAck `Delete` once went to SuppressionService), and an argument that
matches no request field (`device.get(deviceid=...)` once sent an empty `id`).
"""

from __future__ import annotations

import importlib
from typing import Any
from unittest.mock import MagicMock

import pytest
from _discovery import (
    WrapperCase,
    build_all_kwargs,
    discover_cases,
    proto_field,
    proto_sample_body,
    proto_sample_value,
    recorded_grpc_route,
)
from pydantic import BaseModel

from kentik_api.transports.grpc_client import GrpcTransport

ALL_CASES = discover_cases()


class _Stop(Exception):
    """Ends the call once the request is captured, before the response is parsed."""


def _grpc_wrapper(module: Any, wrapper_class: str) -> Any:
    transport = MagicMock(spec=GrpcTransport)
    transport.channel = MagicMock()
    transport.channel.unary_unary.side_effect = lambda path, *a, **kw: path
    return getattr(module, wrapper_class)(transport)


def _capture_rpc(monkeypatch: pytest.MonkeyPatch, module: Any) -> dict[str, Any]:
    captured: dict[str, Any] = {}

    def _call_grpc(rpc_path, request, *, api_config=None, error_cls=None):
        captured["rpc_path"] = rpc_path
        captured["request"] = request
        raise _Stop

    monkeypatch.setattr(module, "call_grpc", _call_grpc)
    return captured


@pytest.mark.parametrize(
    "case",
    ALL_CASES,
    ids=[f"{case.wrapper_class}.{case.method_name}" for case in ALL_CASES],
)
def test_every_argument_reaches_a_field_of_its_own_rpc(
    case: WrapperCase, monkeypatch: pytest.MonkeyPatch
):
    module = importlib.import_module(case.module_path)
    if not hasattr(module, "build_grpc_request"):
        assert not (case.file_path.parents[1] / "pb").exists()
        assert recorded_grpc_route(case) is None
        return
    wrapper = _grpc_wrapper(module, case.wrapper_class)
    method = getattr(wrapper, case.method_name)
    kwargs = build_all_kwargs(method)

    built: dict[str, Any] = {}
    real_build = module.build_grpc_request

    def _build(message_cls, body, fields, update_mask_from=None):
        descriptor = message_cls.DESCRIPTOR
        built["raw_body"] = body
        body = proto_sample_body(descriptor, body)
        built.update(
            message_cls=message_cls,
            body=body,
            fields=fields,
            update_mask_from=update_mask_from,
        )
        built["request"] = real_build(
            message_cls,
            body,
            {
                path: proto_sample_value(proto_field(descriptor, path), value)
                if proto_field(descriptor, path) is not None
                else value
                for path, value in fields.items()
            },
            update_mask_from,
        )
        return built["request"]

    monkeypatch.setattr(module, "build_grpc_request", _build)
    captured = _capture_rpc(monkeypatch, module)

    try:
        method(**kwargs)
    except _Stop:
        pass
    except NotImplementedError as exc:
        assert "not yet implemented" in str(exc)
        assert recorded_grpc_route(case) is None, (
            f"api_surface.json routes this method to {recorded_grpc_route(case)}"
        )
        return

    assert captured["rpc_path"].endswith(f".{recorded_grpc_route(case)}")

    request_descriptor = built["message_cls"].DESCRIPTOR
    service_name, rpc_name = captured["rpc_path"].rsplit(".", 1)[1].split("/")
    rpc = request_descriptor.file.services_by_name[service_name].methods_by_name[
        rpc_name
    ]
    rest_module = getattr(module, case.rest_module_alias).__name__.rsplit(".", 1)[1]
    assert service_name == rest_module
    assert rpc.input_type is request_descriptor

    fields = built["fields"]
    unresolved = [
        path for path in fields if proto_field(request_descriptor, path) is None
    ]
    assert not unresolved, f"no {request_descriptor.name} field for {unresolved}"

    arguments = {
        name: value
        for name, value in kwargs.items()
        if name not in ("api_config_override", "data")
    }
    assert len(fields) == len(arguments)
    for name, value in arguments.items():
        assert any(v is value for v in fields.values()), f"{name} is not sent"
    assert (built["body"] is not None) == ("data" in kwargs)
    if "data" in kwargs:
        data = kwargs["data"]
        if isinstance(data, BaseModel):
            assert data.model_fields_set == set(type(data).model_fields)
        sent = (
            data.model_dump(by_alias=True, exclude_unset=True)
            if isinstance(data, BaseModel)
            else dict(data)
        )
        raw = built["raw_body"]
        assert raw == sent or list(raw.values()) == [sent], "the body is not the data"
    assert not _unset_paths(built["request"], built["body"] or {}), (
        "body fields sent but not set in the request"
    )
    if built["update_mask_from"]:
        mask = request_descriptor.fields_by_name["update_mask"]
        assert mask.message_type.full_name == "google.protobuf.FieldMask"
        assert built["update_mask_from"] in request_descriptor.fields_by_name
        assert set(built["body"]) == {built["update_mask_from"]}


def _unset_paths(message: Any, body: dict[str, Any], prefix: str = "") -> list[str]:
    """Lists the body keys with a value whose field the built message leaves unset."""
    set_names = {field.name for field, _ in message.ListFields()}
    unset: list[str] = []
    for key, value in body.items():
        if value in (None, [], {}):
            continue
        field = proto_field(message.DESCRIPTOR, key)
        path = f"{prefix}{key}"
        if field is None or field.name not in set_names:
            unset.append(path)
            continue
        child = getattr(message, field.name)
        if field.message_type is None or field.message_type.GetOptions().map_entry:
            continue
        if field.message_type.full_name.startswith("google.protobuf."):
            continue
        if isinstance(value, list):
            child, value = child[0], value[0]
        if isinstance(value, dict):
            unset += _unset_paths(child, value, f"{path}.")
    return unset


def _sent_device_request(monkeypatch, method_name: str, **kwargs) -> Any:
    module = importlib.import_module("kentik_api.gen.device.services.device")
    wrapper = _grpc_wrapper(module, "DeviceServiceWrapper")
    captured = _capture_rpc(monkeypatch, module)
    with pytest.raises(_Stop):
        getattr(wrapper, method_name)(**kwargs)
    return captured


def test_get_device_sends_the_id_and_query_options(monkeypatch):
    sent = _sent_device_request(
        monkeypatch, "get", deviceid="42", querynoCustomColumns=True
    )

    assert sent["rpc_path"].endswith("DeviceService/GetDevice")
    assert sent["request"].id == "42"
    assert sent["request"].query.no_custom_columns is True


def test_delete_device_sends_the_id(monkeypatch):
    sent = _sent_device_request(monkeypatch, "delete", deviceid="42")

    assert sent["rpc_path"].endswith("DeviceService/DeleteDevice")
    assert sent["request"].id == "42"
