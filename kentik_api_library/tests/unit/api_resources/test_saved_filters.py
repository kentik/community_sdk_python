from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.saved_filters_api import SavedFiltersAPI
from kentik_api.public.saved_filter import Filter, FilterGroups, Filters, SavedFilter
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_saved_filter_success() -> None:
    # given
    create_response_payload = """
    {
        "filter_name":"test_filter1",
        "filter_description":"This is test filter description",
        "filters": {
            "connector":"All",
            "filterGroups": [
                {
                    "connector":"All",
                    "filters": [
                        {
                            "filterField":"dst_as",
                            "filterValue":"81",
                            "operator":"="
                        }],
                    "not":false
                }]
            },
        "company_id":"74333",
        "filter_level":"company",
        "edate":"2020-12-26T10:46:13.095Z",
        "cdate":"2020-12-16T10:46:13.095Z",
        "id":8152
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    saved_filters_api = SavedFiltersAPI(connector)

    # when
    filter_ = Filter(filterField="dst_as", filterValue="81", operator="=")
    filter_groups = [FilterGroups(connector="All", not_=False, filters=[filter_])]
    filters = Filters(connector="All", filterGroups=filter_groups)
    to_create = SavedFilter(
        filter_name="test_filter1",
        filters=filters,
        filter_description="This is test filter description",
    )
    created = saved_filters_api.create(to_create)

    # then
    assert connector.last_url_path == "/saved-filter/custom"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["filter_name"] == "test_filter1"
    assert connector.last_payload["filter_description"] == "This is test filter description"
    assert connector.last_payload["filters"]["connector"] == "All"
    assert connector.last_payload["filters"]["filterGroups"][0]["connector"] == "All"
    assert connector.last_payload["filters"]["filterGroups"][0]["not"] is False
    assert connector.last_payload["filters"]["filterGroups"][0]["filters"][0]["filterField"] == "dst_as"

    assert created.id == ID(8152)
    assert created.filter_name == "test_filter1"
    assert created.filter_description == "This is test filter description"
    assert created.company_id == ID(74333)
    assert created.filter_level == "company"
    assert created.created_date == "2020-12-16T10:46:13.095Z"
    assert created.updated_date == "2020-12-26T10:46:13.095Z"
    assert created.filters is not None
    assert created.filters.connector == "All"
    assert created.filters.filterGroups[0].connector == "All"
    assert created.filters.filterGroups[0].not_ is False
    assert created.filters.filterGroups[0].filters[0].filterField == "dst_as"
    assert created.filters.filterGroups[0].filters[0].filterValue == "81"
    assert created.filters.filterGroups[0].filters[0].operator == "="


def test_get_saved_filter_success() -> None:
    # given
    get_response_payload = """
        {
            "id":8153,
            "company_id":"74333",
            "filters":{
                    "connector":"All",
                    "filterGroups":[
                        {
                            "connector":"All",
                            "filters":[{
                                    "filterField":"dst_as",
                                    "filterValue":"81",
                                    "operator":"="
                                }],
                            "not":false
                        }]
                },
            "filter_name":"test_filter1",
            "filter_description":"This is test filter description",
            "cdate":"2020-12-16T11:26:18.578Z",
            "edate":"2020-12-26T11:26:19.187Z",
            "filter_level":"company"
        }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    saved_filters_api = SavedFiltersAPI(connector)
    filter_id = ID(8153)

    # when
    saved_filter = saved_filters_api.get(filter_id)

    # then
    assert connector.last_url_path == f"/saved-filter/custom/{filter_id}"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert saved_filter.id == ID(8153)
    assert saved_filter.filter_name == "test_filter1"
    assert saved_filter.filter_description == "This is test filter description"
    assert saved_filter.company_id == ID(74333)
    assert saved_filter.filter_level == "company"
    assert saved_filter.created_date == "2020-12-16T11:26:18.578Z"
    assert saved_filter.updated_date == "2020-12-26T11:26:19.187Z"
    assert saved_filter.filters is not None
    assert saved_filter.filters.connector == "All"
    assert saved_filter.filters.filterGroups[0].connector == "All"
    assert saved_filter.filters.filterGroups[0].not_ is False
    assert saved_filter.filters.filterGroups[0].filters[0].filterField == "dst_as"
    assert saved_filter.filters.filterGroups[0].filters[0].filterValue == "81"
    assert saved_filter.filters.filterGroups[0].filters[0].operator == "="


def test_update_saved_filter_success() -> None:
    # given
    update_response_payload = """
            {
                "id":8153,
                "company_id":"74333",
                "filters":{
                        "connector":"All",
                        "filterGroups":[
                            {
                                "connector":"All",
                                "filters":[{
                                        "filterField":"dst_as",
                                        "filterValue":"81",
                                        "operator":"="
                                    }],
                                "not":false
                            }]
                    },
                "filter_name":"test_filter1",
                "filter_description":"Updated Saved Filter description",
                "cdate":"2020-12-16T11:26:18.578Z",
                "edate":"2020-12-16T11:26:19.187Z",
                "filter_level":"company"
            }"""
    connector = StubAPIConnector(update_response_payload, HTTPStatus.OK)
    saved_filters_api = SavedFiltersAPI(connector)

    # when
    filter_id = ID(8153)
    filter_ = Filter(filterField="dst_as", filterValue="81", operator="=")
    filter_groups = [FilterGroups(connector="All", not_=False, filters=[filter_])]
    filters = Filters(connector="All", filterGroups=filter_groups)
    to_update = SavedFilter(
        filter_name="test_filter1",
        filters=filters,
        id=filter_id,
        filter_description="Updated Saved Filter description",
    )
    updated = saved_filters_api.update(to_update)

    # then
    assert connector.last_url_path == f"/saved-filter/custom/{filter_id}"
    assert connector.last_method == APICallMethods.PUT
    assert connector.last_payload is not None

    assert updated.filter_description == "Updated Saved Filter description"


def test_delete_saved_filter_success() -> None:
    # given
    delete_response_payload = ""  # deleting user responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    saved_filters_api = SavedFiltersAPI(connector)

    # when
    filter_id = ID(8153)
    delete_successful = saved_filters_api.delete(filter_id)

    # then
    assert connector.last_url_path == f"/saved-filter/custom/{filter_id}"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None
    assert delete_successful is True
