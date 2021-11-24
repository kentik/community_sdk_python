from http import HTTPStatus

from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.api_resources.tenants_api import MyKentikPortalAPI
from kentik_api.public.types import ID
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_tenant_user_success() -> None:
    # given
    create_response_payload = """
    {
        "id":"148148",
        "user_email":"user2@testtenant.com",
        "last_login":null,
        "tenant_id":"577",
        "company_id":"74333"
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    my_kentik_portal_api = MyKentikPortalAPI(connector)

    # when
    to_create_email = "user2@testtenant.com"
    tenant_id = ID(577)
    created = my_kentik_portal_api.create_tenant_user(tenant_id, to_create_email)

    # then
    assert connector.last_url_path == "/mykentik/tenant/577/user"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["user"]["user_email"] == "user2@testtenant.com"

    assert created.id == ID(148148)
    assert created.email == "user2@testtenant.com"
    assert created.last_login is None
    assert created.tenant_id == ID(577)
    assert created.company_id == ID(74333)


def test_get_tenant_success() -> None:
    # given
    get_response_payload = """
    {
        "id":577,
        "name":"test_tenant",
        "description":"This is test tenant",
        "users": [
            {
                "id":"148099",
                "user_email":"test@tenant.user",
                "last_login":null,
                "tenant_id":"577",
                "company_id":"74333"
            },{
                "id":"148113",
                "user_email":"user@testtenant.com",
                "last_login":null,
                "tenant_id":"577",
                "company_id":"74333"
            }],
        "created_date":"2020-12-21T10:55:52.449Z",
        "updated_date":"2020-12-22T10:55:52.449Z"
    }"""
    connector = StubAPIConnector(get_response_payload, HTTPStatus.OK)
    my_kentik_portal_api = MyKentikPortalAPI(connector)
    tenant_id = ID(577)

    # when
    tenant = my_kentik_portal_api.get(tenant_id)

    # then
    assert connector.last_url_path == f"/mykentik/tenant/577"
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert tenant.id == ID(577)
    assert tenant.name == "test_tenant"
    assert tenant.description == "This is test tenant"
    assert tenant.users[0].id == ID(148099)
    assert tenant.users[1].id == ID(148113)
    assert tenant.created_date == "2020-12-21T10:55:52.449Z"
    assert tenant.updated_date == "2020-12-22T10:55:52.449Z"


def test_delete_tenant_user_success() -> None:
    # given
    delete_response_payload = ""  # deleting user responds with empty body
    connector = StubAPIConnector(delete_response_payload, HTTPStatus.NO_CONTENT)
    my_kentik_portal_api = MyKentikPortalAPI(connector)

    # when
    tenant_id = ID(577)
    tenant_user_id = ID(148099)
    delete_successful = my_kentik_portal_api.delete_tenant_user(tenant_id, tenant_user_id)

    # then
    assert connector.last_url_path == f"/mykentik/tenant/577/user/148099"
    assert connector.last_method == APICallMethods.DELETE
    assert connector.last_payload is None
    assert delete_successful is True
