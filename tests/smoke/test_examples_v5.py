# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""The ported V5 examples run end to end against a mocked API (spec 005, FR-024)."""

from __future__ import annotations

import base64

import httpx
import pytest
import respx

from examples.v5 import batch, query

_V5 = "https://api.kentik.com/api/v5"


@pytest.fixture(autouse=True)
def credentials(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("KENTIK_EMAIL", "dev@example.com")
    monkeypatch.setenv("KENTIK_API_TOKEN", "token")


@respx.mock
def test_the_query_example_runs(capsys: pytest.CaptureFixture[str]):
    respx.get(url__regex=r"https://grpc\.api\.kentik\.com/device/.*").respond(
        200, json={"devices": [{"id": "1", "deviceName": "router1"}]}
    )
    data = respx.post(f"{_V5}/query/topXdata").respond(
        200, json={"results": [{"bucket": "Left +Y Axis", "data": [{"key": "a"}]}]}
    )
    respx.post(f"{_V5}/query/url").respond(200, json="https://portal.kentik.com/x")
    png = base64.b64encode(b"\x89PNG").decode()
    respx.post(f"{_V5}/query/topXchart").respond(
        200, json={"dataUri": f"data:image/png;base64,{png}"}
    )

    query.main()

    sent = data.calls.last.request
    assert b'"device_name":"router1"' in sent.content.replace(b" ", b"")
    out = capsys.readouterr().out
    assert "Left +Y Axis: 1 row(s)" in out
    assert "Chart: image/png, 4 bytes" in out


@respx.mock
def test_the_query_example_reports_a_chart_timeout(capsys):
    respx.get(url__regex=r"https://grpc\.api\.kentik\.com/device/.*").respond(
        200, json={"devices": []}
    )
    respx.post(f"{_V5}/query/topXdata").respond(200, json={"results": []})
    respx.post(f"{_V5}/query/url").respond(200, json="https://portal.kentik.com/x")
    respx.post(f"{_V5}/query/topXchart").mock(
        side_effect=httpx.ReadTimeout("no answer")
    )

    query.main()

    assert "did not answer" in capsys.readouterr().out


@respx.mock
def test_the_batch_example_sends_only_when_asked(capsys):
    tags = respx.post(f"{_V5}/batch/tags").respond(
        202, json={"message": "queued", "guid": "g-1"}
    )
    respx.get(f"{_V5}/batch/g-1/status").respond(
        200,
        json={
            "guid": "g-1",
            "is_complete": True,
            "upserts": {"applied": 1},
            "deletes": {"applied": 1},
        },
    )

    batch.main([])
    assert not tags.called

    batch.main(["--send"])
    assert tags.call_count == 1
    assert b'"replace_all":false' in tags.calls.last.request.content.replace(b" ", b"")
    assert "upserts applied: 1" in capsys.readouterr().out


@respx.mock
def test_the_analytics_example_runs(capsys):
    from examples.v5 import analytics_topx

    respx.get(url__regex=r"https://grpc\.api\.kentik\.com/device/.*").respond(
        200, json={"devices": [{"id": "1", "deviceName": "router1"}]}
    )
    respx.get(url__regex=r"https://grpc\.api\.kentik\.com/interface/.*").respond(
        200,
        json={
            "interfaces": [
                {"deviceId": "1", "interfaceDescription": "eth0", "snmpSpeed": 1000}
            ]
        },
    )
    flow = [[1760572800000 + i * 300000, 5e8, 300] for i in range(36)]
    data = respx.post(f"{_V5}/query/topXdata").respond(
        200,
        json={
            "results": [
                {
                    "bucket": "flow",
                    "data": [
                        {
                            "key": "k",
                            "i_device_name": "router1",
                            "output_port": "eth0 : Uplink",
                            "avg_bits_per_sec": 5e8,
                            "timeSeries": {"both_bits_per_sec": {"flow": flow}},
                        }
                    ],
                }
            ]
        },
    )

    analytics_topx.main()

    sent = data.calls.last.request.content.replace(b" ", b"")
    assert b'"device_name":"router1"' in sent
    out = capsys.readouterr().out
    assert "Got 36 entries" in out
    assert "router1:eth0" in out
