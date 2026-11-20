# HAND-WRITTEN: not modified by `uv run poe generate`. Edit directly.
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.generation.public_names import (
    NameDriftError,
    PublicNames,
    default_model_name,
    model_key,
    operation_key,
)


@pytest.mark.parametrize(
    ("method", "path", "expected"),
    [
        ("get", "/label/v202210/labels/{id}", "GET /label/<version>/labels/{}"),
        ("post", "/v1/customdimension", "POST /<version>/customdimension"),
        ("get", "/asset_tags/v20260515beta1/keys", "GET /asset_tags/<version>/keys"),
        ("get", "/dictionary/v20260604alpha1", "GET /dictionary/<version>"),
        ("post", "/routes/list", "POST /routes/list"),
    ],
)
def test_operation_key_ignores_versions_and_parameter_names(method, path, expected):
    assert operation_key(method, path) == expected


@pytest.mark.parametrize(
    ("name", "key", "default"),
    [
        ("labelv202210Label", "label<version>Label", "Label"),
        ("v202303Severity", "<version>Severity", "Severity"),
        ("v202312alpha1Secret", "<version>Secret", "Secret"),
        ("devicev202504beta2Label", "device<version>Label", "Label"),
        ("Ipv4Address", "Ipv4Address", "Ipv4Address"),
        ("rpcStatus", "rpcStatus", "rpcStatus"),
    ],
)
def test_model_key_and_default_name(name, key, default):
    assert model_key(name) == key
    assert default_model_name(name) == default


def _seeded() -> PublicNames:
    names = PublicNames()
    names.services(["label"])
    names.methods("label", {"GET /label/<version>/labels": "list_labels"})
    names.models("label", ["labelv202210Label", "ListLabelsResponse"])
    return names


def test_a_round_trip_through_the_file_keeps_every_name(tmp_path: Path):
    path = tmp_path / "public_names.json"
    _seeded().save(path)
    names = PublicNames.load(path)

    assert names.services(["label"]) == {"label": "label"}
    assert names.methods("label", {"GET /label/<version>/labels": "other"}) == {
        "GET /label/<version>/labels": "list_labels"
    }
    names.save(path)
    assert PublicNames.load(path)._services == _seeded()._services


def test_a_version_bump_keeps_every_name():
    names = _seeded()
    assert names.models("label", ["labelv202604Label", "ListLabelsResponse"]) == {
        "labelv202604Label": "Label",
        "ListLabelsResponse": "ListLabelsResponse",
    }


def test_a_new_model_never_takes_an_existing_name():
    names = _seeded()
    with pytest.raises(NameDriftError, match="default name `Label` is taken"):
        names.models("label", ["labelv202210Label", "Label", "ListLabelsResponse"])


def test_an_unversioned_model_claims_its_name_before_a_stripped_one():
    renamed = PublicNames().models(
        "alerting", ["v202505AlertAcknowledgement", "AlertAcknowledgement"]
    )
    assert renamed == {
        "AlertAcknowledgement": "AlertAcknowledgement",
        "v202505AlertAcknowledgement": "v202505AlertAcknowledgement",
    }


def test_an_upstream_rename_fails_and_names_the_entry_and_the_candidate():
    names = _seeded()
    with pytest.raises(NameDriftError) as error:
        names.methods("label", {"GET /label/<version>/labels:list": "list_labels"})
    message = str(error.value)
    assert "`list_labels` ('GET /label/<version>/labels')" in message
    assert "'GET /label/<version>/labels:list'" in message


def test_repointing_the_entry_keeps_the_public_name():
    names = _seeded()
    names._services["label"]["methods"]["list_labels"] = (
        "GET /label/<version>/labels:list"
    )
    assert names.methods("label", {"GET /label/<version>/labels:list": "x"}) == {
        "GET /label/<version>/labels:list": "list_labels"
    }


def test_a_removed_service_fails_until_its_entry_is_deleted():
    names = _seeded()
    with pytest.raises(NameDriftError, match="`label` \\('label'\\)"):
        names.services(["labels"])
    names._services["label"]["upstream"] = "labels"
    assert names.services(["labels"]) == {"labels": "label"}


def test_a_service_without_operations_fails_when_it_had_methods():
    with pytest.raises(NameDriftError, match="list_labels"):
        _seeded().methods("label", {})


def test_a_taken_default_method_name_fails():
    names = _seeded()
    with pytest.raises(NameDriftError, match="default name `list_labels` is taken"):
        names.methods(
            "label",
            {
                "GET /label/<version>/labels": "list_labels",
                "GET /label/<version>/all": "list_labels",
            },
        )


def test_two_entries_for_one_operation_fail():
    names = _seeded()
    names._services["label"]["methods"]["labels"] = "GET /label/<version>/labels"
    with pytest.raises(NameDriftError, match="both point at"):
        names.methods("label", {"GET /label/<version>/labels": "list_labels"})


def test_models_that_differ_only_by_version_fail():
    with pytest.raises(NameDriftError, match="differ only by version"):
        PublicNames().models("alerting", ["v202303TimeRange", "v202501TimeRange"])


@pytest.mark.parametrize(
    "services",
    [
        {"class": {"upstream": "x"}},
        {"pb_companions": {"upstream": "x"}},
        {"label": {"upstream": "label", "methods": {"_hidden": "GET /x"}}},
        {"label": {"upstream": "label", "models": {"Bad-Name": "x"}}},
    ],
)
def test_unusable_names_are_rejected(services):
    with pytest.raises(ValueError):
        PublicNames(services)


def test_a_v6_query_service_arrives_without_changing_a_v5_name():
    from scripts.generation.public_names import NAMES_FILE

    names = PublicNames.load(NAMES_FILE)
    before = json.loads(json.dumps(names._services["v5"]))
    upstream = [entry["upstream"] for entry in names._services.values()]

    services = names.services([*upstream, "query"])
    v5_methods = names.methods(
        "v5", {key: "other" for key in before["methods"].values()}
    )
    query_methods = names.methods("query", {"POST /query/<version>/data": "query_data"})

    assert services["v5"] == "v5"
    assert services["query"] == "query"
    assert v5_methods == {key: name for name, key in before["methods"].items()}
    assert query_methods == {"POST /query/<version>/data": "query_data"}
    assert names._services["v5"] == before
