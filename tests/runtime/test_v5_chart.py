# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""decode_chart() turns a V5 chart response into image bytes (spec 005, FR-004)."""

from __future__ import annotations

import base64

import pytest

from kentik_api.errors import HTTPException
from kentik_api.gen.v5.models import ChartResponse
from kentik_api.v5_tools import ChartImage, decode_chart

_SVG = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
_PNG = b"\x89PNG\r\n\x1a\nrest"


@pytest.mark.parametrize(
    ("mime", "data"), [("image/svg+xml", _SVG), ("image/png", _PNG)]
)
def test_a_data_uri_decodes_to_bytes_and_type(mime: str, data: bytes):
    uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"

    assert decode_chart(ChartResponse(dataUri=uri)) == ChartImage(mime, data)


@pytest.mark.parametrize(
    ("uri", "problem"),
    [
        (None, "no data URI"),
        ("https://portal.kentik.com/chart.png", "not a base64 data URI"),
        ("data:image/png;base64,@@@not-base64@@@", "not valid base64"),
    ],
)
def test_an_unusable_data_uri_is_a_clear_502(uri, problem: str):
    with pytest.raises(HTTPException) as exc:
        decode_chart(ChartResponse(dataUri=uri))

    assert exc.value.status_code == 502
    assert problem in exc.value.message
