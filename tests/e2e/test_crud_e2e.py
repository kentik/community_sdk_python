# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
"""Live create, read, update, and delete round trips. MUTATING: writes to the real account.

Each test creates one disposable object named `sdk-e2e-test-<hex>`, records it
in the ledger (tests/e2e/ledger.py) before anything else, updates it, deletes
it, and makes sure that it is gone. Update and delete go through
`ledger.owned()`, so a test can change only an object it created. When a test
fails halfway, the session teardown deletes what it left; whatever still
fails stays in the ledger for `uv run poe e2e-cleanup`.

Every test runs on the REST and the gRPC client. IP values come from
TEST-NET-1 (192.0.2.0/24, RFC 5737), so no object matches real traffic.

A strict xfail marks each call that failed live for every payload tried. When
the cause is fixed, the xfail turns into a failure, and the marker can go.

Opt-in twice: `uv run poe test-e2e-mutating`, or
`pytest -m e2e_mutating --run-live-e2e tests/e2e/test_crud_e2e.py`.
"""

from __future__ import annotations

import time
from collections.abc import Callable

import pytest
from ledger import KINDS, Ledger

from kentik_api.client import KentikAPI
from kentik_api.errors import HTTPException
from kentik_api.gen.as_group.models import (
    ASGroupConcise,
    ASGroupServiceUpdateASGroupBody,
    CreateASGroupRequest,
)
from kentik_api.gen.custom_application.models import CustomApplication
from kentik_api.gen.flow_tag.models import (
    AddressInfo,
    CreateFlowTagRequest,
    FlowTag,
    FlowTagServiceUpdateFlowTagBody,
)
from kentik_api.gen.label.models import (
    CreateLabelRequest,
    Label,
    LabelServiceUpdateLabelBody,
)
from kentik_api.gen.saved_filter.models import (
    FilterField,
    FilterLevel,
    FilterOperator,
    SavedFilter,
    SavedFilterFilter,
    SavedFilterFilterGroup,
    SavedFilterFilters,
)
from kentik_api.gen.site.models import (
    CreateSiteMarketRequest,
    CreateSiteRequest,
    Site,
    SiteMarket,
    SiteServiceUpdateSiteBody,
    SiteServiceUpdateSiteMarketBody,
    SiteType,
)

pytestmark = pytest.mark.e2e_mutating


def _known_failure(
    request: pytest.FixtureRequest, *transports: str, reason: str
) -> None:
    if request.node.callspec.params["any_client"] in transports:
        request.applymarker(
            pytest.mark.xfail(raises=HTTPException, strict=True, reason=reason)
        )


def _assert_gone(client: KentikAPI, kind: str, id: str) -> None:
    with pytest.raises(HTTPException):
        KINDS[kind].get(client, id)


def _read_back[T](get: Callable[[], T]) -> T:
    # The live API sometimes reports an object it just wrote as missing for a moment.
    for attempt in range(5):
        try:
            return get()
        except HTTPException:
            if attempt == 4:
                raise
            time.sleep(1)
    raise AssertionError("unreachable")


def test_label_lifecycle(any_client: KentikAPI, ledger: Ledger):
    name = ledger.new_name()
    created = any_client.label.create(
        data=CreateLabelRequest(label=Label(name=name, color="#5289D9"))
    )
    assert created.label is not None
    id = ledger.created("label", created.label.id, name)
    assert created.label.name == name

    new_name = ledger.new_name()
    updated = any_client.label.update(
        id=ledger.owned("label", id),
        data=LabelServiceUpdateLabelBody(label={"name": new_name, "color": "#E35B5B"}),
    )
    assert updated.label is not None
    assert updated.label.name == new_name

    listed = {lb.id: lb for lb in any_client.label.list().labels or [] if lb}
    assert listed[id].name == new_name

    ledger.delete(any_client, "label", id)
    _assert_gone(any_client, "label", id)


def test_site_market_lifecycle(any_client: KentikAPI, ledger: Ledger):
    name = ledger.new_name()
    created = any_client.site.create_market(
        data=CreateSiteMarketRequest(
            siteMarket=SiteMarket(name=name, description="created by an SDK e2e test")
        )
    )
    assert created.siteMarket is not None
    id = ledger.created("site_market", created.siteMarket.id, name)

    any_client.site.update_market(
        id=ledger.owned("site_market", id),
        data=SiteServiceUpdateSiteMarketBody(
            siteMarket={"name": name, "description": "updated by an SDK e2e test"}
        ),
    )
    got = _read_back(lambda: any_client.site.get_market(id=id).siteMarket)
    assert got is not None
    assert got.description == "updated by an SDK e2e test"

    ledger.delete(any_client, "site_market", id)
    _assert_gone(any_client, "site_market", id)


def test_site_lifecycle(any_client: KentikAPI, ledger: Ledger):
    name = ledger.new_name()
    created = any_client.site.create(
        data=CreateSiteRequest(
            site=Site(title=name, type=SiteType.SITE_TYPE_OTHER, lat=0.0, lon=0.0)
        )
    )
    assert created.site is not None
    id = ledger.created("site", created.site.id, name)

    any_client.site.update(
        id=ledger.owned("site", id),
        data=SiteServiceUpdateSiteBody(
            site={"title": name, "type": "SITE_TYPE_BRANCH", "lat": 1.0, "lon": 1.0}
        ),
    )
    got = _read_back(lambda: any_client.site.get(id=id).site)
    assert got is not None
    assert got.type == SiteType.SITE_TYPE_BRANCH

    ledger.delete(any_client, "site", id)
    _assert_gone(any_client, "site", id)


def test_as_group_lifecycle(any_client: KentikAPI, ledger: Ledger):
    # The API rejects unknown ASNs and an ASN that another group holds.
    name = ledger.new_name()
    created = any_client.as_group.create(
        data=CreateASGroupRequest(asGroup=ASGroupConcise(name=name, asn=["36459"]))
    )
    assert created.asGroup is not None
    id = ledger.created("as_group", created.asGroup.id, name)

    any_client.as_group.update(
        asGroupid=ledger.owned("as_group", id),
        data=ASGroupServiceUpdateASGroupBody(
            asGroup={"name": name, "asn": ["36459", "46489"]}
        ),
    )
    got = _read_back(lambda: any_client.as_group.get(asGroupid=id).asGroup)
    assert got is not None
    assert sorted(a.asn for a in got.asn or [] if a and a.asn) == [36459, 46489]

    ledger.delete(any_client, "as_group", id)
    _assert_gone(any_client, "as_group", id)


def test_flow_tag_lifecycle(
    any_client: KentikAPI, ledger: Ledger, request: pytest.FixtureRequest
):
    _known_failure(request, "rest", "grpc", reason="CreateFlowTag answers HTTP 500")
    name = ledger.new_name()
    created = any_client.flow_tag.create(
        data=CreateFlowTagRequest(
            flowTag=FlowTag(name=name, ip=AddressInfo(addresses=["192.0.2.1/32"]))
        )
    )
    assert created.flowTag is not None
    id = ledger.created("flow_tag", created.flowTag.id, name)

    any_client.flow_tag.update(
        flowTagid=ledger.owned("flow_tag", id),
        data=FlowTagServiceUpdateFlowTagBody(
            flowTag={
                "name": name,
                "ip": {"addresses": ["192.0.2.1/32", "192.0.2.2/32"]},
            }
        ),
    )
    got = any_client.flow_tag.get(flowTagid=id).flowTag
    assert got is not None
    assert got.ip is not None
    assert sorted(got.ip.addresses or []) == ["192.0.2.1/32", "192.0.2.2/32"]

    ledger.delete(any_client, "flow_tag", id)
    _assert_gone(any_client, "flow_tag", id)


def _saved_filter(name: str, value: str) -> SavedFilter:
    rule = SavedFilterFilter(
        filterField=FilterField.FILTER_FIELD_INET_DST_ADDR,
        operator=FilterOperator.FILTER_OPERATOR_EQUAL,
        filterValue=value,
    )
    return SavedFilter(
        filterName=name,
        filterDescription="created by an SDK e2e test",
        filterLevel=FilterLevel.FILTER_LEVEL_COMPANY,
        filters=SavedFilterFilters(
            filterGroups=[SavedFilterFilterGroup(filters=[rule])]
        ),
    )


def test_saved_filter_lifecycle(
    any_client: KentikAPI, ledger: Ledger, request: pytest.FixtureRequest
):
    _known_failure(request, "rest", "grpc", reason="CreateSavedFilter answers HTTP 500")
    name = ledger.new_name()
    created = any_client.saved_filter.create(data=_saved_filter(name, "192.0.2.1"))
    assert created.filter is not None
    id = ledger.created("saved_filter", created.filter.id, name)

    any_client.saved_filter.update(
        id=ledger.owned("saved_filter", id), data=_saved_filter(name, "192.0.2.2")
    )
    got = any_client.saved_filter.get(id=id).filter
    assert got is not None
    assert got.filters is not None
    group = got.filters.filterGroups[0]
    assert group.filters
    assert group.filters[0] is not None
    assert group.filters[0].filterValue == "192.0.2.2"

    ledger.delete(any_client, "saved_filter", id)
    _assert_gone(any_client, "saved_filter", id)


def test_custom_application_lifecycle(any_client: KentikAPI, ledger: Ledger):
    name = ledger.new_name()
    created = any_client.custom_application.create(
        data=CustomApplication(
            name=name, ipRange=["192.0.2.0/24"], protocol=[6], port=[8443]
        )
    )
    assert created.application is not None
    id = ledger.created("custom_application", created.application.id, name)

    any_client.custom_application.update(
        customApplicationId=ledger.owned("custom_application", id),
        data=CustomApplication(
            name=name, ipRange=["192.0.2.0/24"], protocol=[6], port=[8444]
        ),
    )
    got = any_client.custom_application.get(customApplicationId=id).application
    assert got is not None
    assert got.port == [8444]

    ledger.delete(any_client, "custom_application", id)
    _assert_gone(any_client, "custom_application", id)
