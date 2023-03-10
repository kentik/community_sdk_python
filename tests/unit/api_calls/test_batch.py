from kentik_api.api_calls.api_call import APICall, APICallMethods
from kentik_api.api_calls.batch import *


def test_flow_tags_batch_operation_return_apiCall():

    # when
    call = flow_tags_batch_operation()

    # then
    assert isinstance(call, APICall)
    assert call.url_path == "/batch/tags"
    assert call.method.name == "POST"


def test_populators_batch_operation_return_apiCall():

    # given
    dimension_name = "dimension"

    # when
    call = populators_batch_operation(dimension_name)

    # then
    assert isinstance(call, APICall)
    assert call.url_path == f"/batch/customdimensions/{dimension_name}/populators"
    assert call.method.name == "POST"


def test_batch_operation_status_return_apiCall():
    # given
    guid = "batch_operation_guid"

    # when
    call = get_batch_operation_status(guid)

    # then
    assert isinstance(call, APICall)
    assert call.url_path == f"/batch/{guid}/status"
    assert call.method.name == "GET"
