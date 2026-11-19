"""Live evidence for reports/upstream/upstream-rest-update-body-merge.md.

MUTATING, on disposable objects only. Every object it creates is named
`sdk-e2e-test-<hex>`, is recorded in the e2e ledger (tests/e2e/ledger.py)
before anything else, and is deleted in `finally`. The checks that need an
existing object in a service where creation fails use an ID that a GET first
proves does not exist, so they cannot change anything.

Usage, from the SDK repo root with lab credentials in .env:

    uv run python reports/scripts/rest-body-merge/live_probe.py
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tests" / "e2e"))

from ledger import Ledger, sweep

from kentik_api.client import KentikAPI
from kentik_api.core.rest_runtime import request_json
from kentik_api.errors import HTTPException
from kentik_api.gen.alerting.models import AlertAutoAckServiceReplaceBody
from kentik_api.gen.as_group.models import (
    ASGroupConcise,
    ASGroupServiceUpdateASGroupBody,
    CreateASGroupRequest,
)
from kentik_api.gen.flow_tag.models import FlowTagServiceUpdateFlowTagBody
from kentik_api.gen.label.models import (
    CreateLabelRequest,
    Label,
    LabelServiceUpdateLabelBody,
)
from kentik_api.gen.site.models import (
    CreateSiteMarketRequest,
    SiteMarket,
    SiteServiceUpdateSiteMarketBody,
)

MISSING_ID = "999999999"


def outcome(label: str, call: Callable[[], object]) -> object | None:
    try:
        result = call()
    except HTTPException as exc:
        print(f"  {label:<58} {exc.status_code} {exc.message}")
        return None
    text = (
        result.model_dump_json(exclude_none=True)
        if isinstance(result, BaseModel)
        else result
    )
    print(f"  {label:<58} OK  {str(text)[:150]}")
    return result


def raw(client: KentikAPI, method: str, path: str, body: dict | None = None):
    return lambda: request_json(
        method=method,
        path=path,
        path_template=path,
        api_config_override=client.api_config,
        query_params={},
        json_body=body,
        header_params={},
        expected_status=200,
        operation_name="probe",
    )


def as_group(rest: KentikAPI, grpc: KentikAPI, ledger: Ledger) -> None:
    print(
        "\nA1. as_group UpdateASGroup: PUT /as_group/v202212/as_group/{as_group.id}, body *"
    )
    name = ledger.new_name()
    created = rest.as_group.create(
        data=CreateASGroupRequest(asGroup=ASGroupConcise(name=name, asn=["36459"]))
    )
    assert created.asGroup is not None
    id = ledger.created("as_group", created.asGroup.id, name)
    path = f"/as_group/v202212/as_group/{id}"
    print(f"  created {id} with REST CreateASGroup, body key asGroup: OK")
    renamed = ledger.new_name()
    outcome(
        "REST SDK, body {asGroup: {...}}",
        lambda: rest.as_group.update(
            asGroupid=ledger.owned("as_group", id),
            data=ASGroupServiceUpdateASGroupBody(
                asGroup={"name": renamed, "asn": ["36459"]}
            ),
        ),
    )
    outcome(
        "REST raw, body {as_group: {...}}",
        raw(rest, "put", path, {"as_group": {"name": renamed, "asn": ["36459"]}}),
    )
    outcome(
        "REST raw, both keys, asGroup.name=A, as_group.name=B",
        raw(
            rest,
            "put",
            path,
            {
                "asGroup": {"name": f"{name}-a", "asn": ["36459"]},
                "as_group": {"name": f"{name}-b", "asn": ["36459"]},
            },
        ),
    )
    outcome(
        "REST GET after the both-keys update", lambda: rest.as_group.get(asGroupid=id)
    )
    outcome(
        "gRPC SDK, same model as the REST SDK call",
        lambda: grpc.as_group.update(
            asGroupid=ledger.owned("as_group", id),
            data=ASGroupServiceUpdateASGroupBody(
                asGroup={"name": name, "asn": ["36459", "46489"]}
            ),
        ),
    )
    outcome("REST GET after the gRPC update", lambda: rest.as_group.get(asGroupid=id))


def site_market(rest: KentikAPI, grpc: KentikAPI, ledger: Ledger) -> None:
    print(
        "\nA2. site UpdateSiteMarket: PUT /site/v202509/site_markets/{site_market.id}, body *"
    )
    name = ledger.new_name()
    created = rest.site.create_market(
        data=CreateSiteMarketRequest(siteMarket=SiteMarket(name=name))
    )
    assert created.siteMarket is not None
    id = ledger.created("site_market", created.siteMarket.id, name)
    path = f"/site/v202509/site_markets/{id}"
    print(f"  created {id} with REST CreateSiteMarket, body key siteMarket: OK")
    outcome(
        "REST SDK, body {siteMarket: {...}}",
        lambda: rest.site.update_market(
            id=ledger.owned("site_market", id),
            data=SiteServiceUpdateSiteMarketBody(
                siteMarket={"name": name, "description": "camel"}
            ),
        ),
    )
    outcome(
        "REST raw, body {site_market: {...}}",
        raw(rest, "put", path, {"site_market": {"name": name, "description": "snake"}}),
    )
    outcome(
        "REST raw, both keys, description camel/snake",
        raw(
            rest,
            "put",
            path,
            {
                "siteMarket": {"name": name, "description": "camel"},
                "site_market": {"name": name, "description": "snake"},
            },
        ),
    )
    outcome("REST GET after the both-keys update", lambda: rest.site.get_market(id=id))
    outcome(
        "gRPC SDK, same model as the REST SDK call",
        lambda: grpc.site.update_market(
            id=ledger.owned("site_market", id),
            data=SiteServiceUpdateSiteMarketBody(
                siteMarket={"name": name, "description": "grpc"}
            ),
        ),
    )
    outcome("REST GET after the gRPC update", lambda: rest.site.get_market(id=id))


def label_control(rest: KentikAPI, ledger: Ledger) -> None:
    print(
        "\nB. Control, label UpdateLabel: POST /label/v202210/labels/{label.id}, body *, key label/label"
    )
    name = ledger.new_name()
    created = rest.label.create(
        data=CreateLabelRequest(label=Label(name=name, color="#5289D9"))
    )
    assert created.label is not None
    id = ledger.created("label", created.label.id, name)
    outcome(
        "REST SDK, body {label: {...}}",
        lambda: rest.label.update(
            id=ledger.owned("label", id),
            data=LabelServiceUpdateLabelBody(
                label={"name": ledger.new_name(), "color": "#E35B5B"}
            ),
        ),
    )


def missing_id(rest: KentikAPI, grpc: KentikAPI) -> None:
    print(f"\nC1. flow_tag UpdateFlowTag with id {MISSING_ID} (no object exists)")
    if (
        outcome("REST GET first", lambda: rest.flow_tag.get(flowTagid=MISSING_ID))
        is not None
    ):
        print("  id exists, skipped")
    else:
        path = f"/flow_tag/v202404alpha1/tag/{MISSING_ID}"
        body = {"name": "sdk-e2e-test-probe", "ip": {"addresses": ["192.0.2.1/32"]}}
        outcome(
            "REST SDK, body {flowTag: {...}}",
            lambda: rest.flow_tag.update(
                flowTagid=MISSING_ID, data=FlowTagServiceUpdateFlowTagBody(flowTag=body)
            ),
        )
        outcome(
            "REST raw, body {flow_tag: {...}}",
            raw(rest, "put", path, {"flow_tag": body}),
        )
        outcome(
            "gRPC SDK",
            lambda: grpc.flow_tag.update(
                flowTagid=MISSING_ID, data=FlowTagServiceUpdateFlowTagBody(flowTag=body)
            ),
        )

    print(
        f"\nC2. alerting AlertAutoAckService.Replace with id {MISSING_ID} (no object exists)"
    )
    if (
        outcome(
            "REST GET first", lambda: rest.alerting.auto_ack_get(autoAckid=MISSING_ID)
        )
        is not None
    ):
        print("  id exists, skipped")
    else:
        path = f"/v202505/alerts/ack/auto/{MISSING_ID}"
        body = {"startTimeAt": "2030-01-01T00:00:00Z"}
        outcome(
            "REST SDK, body {autoAck: {startTimeAt}}",
            lambda: rest.alerting.auto_ack_replace(
                autoAckid=MISSING_ID, data=AlertAutoAckServiceReplaceBody(autoAck=body)
            ),
        )
        outcome(
            "REST raw, body {auto_ack: {startTimeAt}}",
            raw(rest, "patch", path, {"auto_ack": body}),
        )
        outcome(
            "REST raw, body {auto_ack: {start_time_at}}",
            raw(
                rest,
                "patch",
                path,
                {"auto_ack": {"start_time_at": body["startTimeAt"]}},
            ),
        )
        outcome(
            "gRPC SDK",
            lambda: grpc.alerting.auto_ack_replace(
                autoAckid=MISSING_ID, data=AlertAutoAckServiceReplaceBody(autoAck=body)
            ),
        )


def flow_tag_create(rest: KentikAPI, ledger: Ledger) -> None:
    print(
        "\nD. flow_tag CreateFlowTag: POST /flow_tag/v202404alpha1/tag, body *, no path field"
    )
    for key in ("flowTag", "flow_tag"):
        name = ledger.new_name()
        result = outcome(
            f"REST raw, body {{{key}: {{...}}}}",
            raw(
                rest,
                "post",
                "/flow_tag/v202404alpha1/tag",
                {key: {"name": name, "ip": {"addresses": ["192.0.2.1/32"]}}},
            ),
        )
        created = (result or {}).get("flowTag") if isinstance(result, dict) else None
        if created and created.get("id"):
            ledger.created("flow_tag", created["id"], created.get("name") or name)


def main() -> int:
    ledger = Ledger()
    with KentikAPI(protocol="rest") as rest, KentikAPI(protocol="grpc") as grpc:
        try:
            as_group(rest, grpc, ledger)
            site_market(rest, grpc, ledger)
            label_control(rest, ledger)
            missing_id(rest, grpc)
            flow_tag_create(rest, ledger)
        finally:
            failures = sweep(
                rest, ledger, [e for e in ledger.outstanding() if e.run == ledger.run]
            )
            print(f"\nCleanup: {'all objects deleted' if not failures else failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
