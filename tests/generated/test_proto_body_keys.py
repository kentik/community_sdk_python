# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Pins the upstream workaround that sends a body key under its proto name.

The REST layer of some services drops a camelCase body key when the URL sets a
field inside it (AGENTS.md, "Upstream workarounds"). The generator renames those
keys; every other body keeps the documented camelCase name.
"""

from __future__ import annotations

import json

import pytest
import respx

from kentik_api.client import KentikAPI
from kentik_api.gen.alerting.models import AlertAutoAckServiceReplaceBody
from kentik_api.gen.as_group.models import ASGroupServiceUpdateASGroupBody
from kentik_api.gen.flow_tag.models import FlowTagServiceUpdateFlowTagBody
from kentik_api.gen.label.models import LabelServiceUpdateLabelBody
from kentik_api.gen.site.models import SiteServiceUpdateSiteMarketBody

_BASE = "https://grpc.api.kentik.com"

CASES = [
    (
        lambda c: c.as_group.update(
            asGroupid="1", data=ASGroupServiceUpdateASGroupBody(asGroup={"name": "n"})
        ),
        "put",
        "/as_group/v202212/as_group/1",
        "as_group",
    ),
    (
        lambda c: c.site.update_market(
            id="1", data=SiteServiceUpdateSiteMarketBody(siteMarket={"name": "n"})
        ),
        "put",
        "/site/v202509/site_markets/1",
        "site_market",
    ),
    (
        lambda c: c.flow_tag.update(
            flowTagid="1", data=FlowTagServiceUpdateFlowTagBody(flowTag={"name": "n"})
        ),
        "put",
        "/flow_tag/v202404alpha1/tag/1",
        "flow_tag",
    ),
    (
        lambda c: c.alerting.auto_ack_replace(
            autoAckid="1", data=AlertAutoAckServiceReplaceBody(autoAck={"id": "1"})
        ),
        "patch",
        "/v202505/alerts/ack/auto/1",
        "auto_ack",
    ),
    (
        lambda c: c.label.update(
            id="1", data=LabelServiceUpdateLabelBody(label={"name": "n"})
        ),
        "post",
        "/label/v202210/labels/1",
        "label",
    ),
]


@respx.mock
@pytest.mark.parametrize(
    ("call", "method", "path", "key"), CASES, ids=[c[3] for c in CASES]
)
def test_rest_update_sends_the_key_the_server_reads(call, method, path, key):
    route = respx.route(method=method.upper(), url=f"{_BASE}{path}").respond(
        200, json={}
    )

    with KentikAPI(email="dev@example.com", api_token="token", env_file=None) as client:
        call(client)

    assert list(json.loads(route.calls.last.request.content)) == [key]
