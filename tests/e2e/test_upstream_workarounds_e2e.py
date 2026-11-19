# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Canaries for upstream bugs that the SDK works around. MUTATING: writes to the real account.

Each test sends the request the published schema documents, bypassing the
workaround, and is a strict xfail. When upstream fixes the bug, the test passes,
strict xfail turns that into a failure, and the reason names the workaround to
remove (AGENTS.md, "Upstream workarounds").

Run with the other mutating tests: `uv run poe test-e2e-mutating`.
"""

from __future__ import annotations

import grpc
import pytest
from ledger import Ledger

from kentik_api.auth.credentials import KentikCredentials
from kentik_api.client import KentikAPI
from kentik_api.core.rest_runtime import request_json
from kentik_api.errors import HTTPException
from kentik_api.gen.as_group.models import ASGroupConcise, CreateASGroupRequest
from kentik_api.gen.site.models import CreateSiteMarketRequest, SiteMarket

pytestmark = pytest.mark.e2e_mutating


class DeadlineCrashesServer(Exception):
    pass


grpc_deadline_bug = pytest.mark.xfail(
    raises=DeadlineCrashesServer,
    strict=True,
    reason=(
        "Upstream gRPC fails every call with a deadline on this service. If this "
        "passes, remove the service from _NO_SERVER_DEADLINE in "
        "transports/grpc_client.py and update AGENTS.md."
    ),
)


def _send_documented_body(
    client: KentikAPI, path: str, body: dict, *, method: str
) -> dict:
    return request_json(
        method=method,
        path=path,
        path_template=path,
        api_config_override=client.api_config,
        query_params={},
        json_body=body,
        header_params={},
        expected_status=200,
        operation_name="canary",
    )


def test_update_as_group_reads_the_documented_camel_case_body(
    real_client: KentikAPI, ledger: Ledger
):
    used_asns = {
        asn.asn
        for group in real_client.as_group.list().asGroups or []
        if group is not None
        for asn in group.asn or []
        if asn is not None and asn.asn is not None
    }
    asn = next(
        (
            str(candidate)
            for candidate in (36459, 46489, 13335, 15169, 16509, 8075, 32934, 14061)
            if candidate not in used_asns
        ),
        None,
    )
    if asn is None:
        pytest.skip("All candidate ASNs are already assigned to an AS group")

    name = ledger.new_name()
    created = real_client.as_group.create(
        data=CreateASGroupRequest(asGroup=ASGroupConcise(name=name, asn=[asn]))
    )
    assert created.asGroup is not None
    as_group_id = ledger.owned(
        "as_group", ledger.created("as_group", created.asGroup.id, name)
    )

    body = {"asGroup": {"name": name, "asn": [asn]}}
    try:
        _send_documented_body(
            real_client,
            f"/as_group/v202212/as_group/{as_group_id}",
            body,
            method="put",
        )
    except HTTPException as exc:
        if exc.status_code == 400 and "request.as_group.name" in exc.message:
            pytest.xfail(f"Upstream REST drops the documented body key: {exc.message}")
        raise
    pytest.fail("The documented AS group body was accepted; review the workaround")


def test_update_site_market_reads_the_documented_camel_case_body(
    real_client: KentikAPI, ledger: Ledger
):
    name = ledger.new_name()
    created = real_client.site.create_market(
        data=CreateSiteMarketRequest(siteMarket=SiteMarket(name=name))
    )
    assert created.siteMarket is not None
    site_market_id = ledger.owned(
        "site_market", ledger.created("site_market", created.siteMarket.id, name)
    )

    body = {"siteMarket": {"name": name, "description": "camel"}}
    try:
        _send_documented_body(
            real_client,
            f"/site/v202509/site_markets/{site_market_id}",
            body,
            method="put",
        )
    except HTTPException as exc:
        if exc.status_code == 500 and "TypeError" in exc.message:
            pytest.xfail(
                f"Upstream REST rejects the documented body key: {exc.message}"
            )
        raise
    pytest.fail("The documented site market body was accepted; review the workaround")


@grpc_deadline_bug
@pytest.mark.parametrize(
    "method",
    [
        "/kentik.alerting.public.v202505.MitigationMethodsService/List",
        "/kentik.audit.public.v202601.AuditService/ListAuditEvents",
        "/kentik.custom_application.v202501alpha1.CustomApplicationService/ListCustomApplications",
        "/kentik.custom_dimension.v202411alpha1.CustomDimensionService/ListCustomDimensions",
        "/kentik.plan.v202501alpha1.PlanService/ListPlans",
        "/kentik.saved_filter.v202501alpha1.SavedFilterService/ListSavedFilters",
    ],
)
def test_grpc_call_with_a_deadline_succeeds(real_client: KentikAPI, method: str):
    config = real_client.api_config
    assert config.auth_email and config.auth_token
    plugin = KentikCredentials(config.auth_email, config.auth_token).get_grpc_plugin()
    credentials = grpc.composite_channel_credentials(
        grpc.ssl_channel_credentials(), grpc.metadata_call_credentials(plugin)
    )
    # A plain channel: the SDK's own channel would not send the deadline.
    with grpc.secure_channel("grpc.api.kentik.com:443", credentials) as channel:
        call = channel.unary_unary(
            method,
            request_serializer=lambda _: b"",
            response_deserializer=lambda raw: raw,
        )
        try:
            call(b"", timeout=30)
        except grpc.RpcError as exc:
            details = exc.details() or ""  # ty: ignore[missing-attribute]
            if "name:RangeError" in details:
                raise DeadlineCrashesServer(details) from exc
            raise
