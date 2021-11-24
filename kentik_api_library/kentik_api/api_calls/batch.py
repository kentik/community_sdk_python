from kentik_api.api_calls.api_call import APICall
from kentik_api.api_calls.api_call_decorators import get, payload_type, post


@post
@payload_type(dict)
def flow_tags_batch_operation() -> APICall:
    """Returns batch API call to tags endpoint"""
    return APICall("/batch/tags")


@post
@payload_type(dict)
def populators_batch_operation(dimension_name: str) -> APICall:
    """Returns batch API call to custom dimensions populators endpoint"""
    url_path = f"/batch/customdimensions/{dimension_name}/populators"
    return APICall(url_path)


@get
def get_batch_operation_status(batch_operation_guid: str) -> APICall:
    """Returns batch API call which provides status of batch operation specified by its guid"""
    url_path = f"/batch/{batch_operation_guid}/status"
    return APICall(url_path)
