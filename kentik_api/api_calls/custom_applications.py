# Local application imports
from kentik_api.api_calls.api_call import APICall, ResourceID
from kentik_api.api_calls.api_call_decorators import delete, get, payload_type, post, put


@get
def get_custom_applications() -> APICall:
    """Returns an array of customApplication objects that each contain
    information about an individual customApplication."""
    return APICall("/customApplications")


@post
@payload_type(dict)
def create_custom_application() -> APICall:
    """Creates and returns a custocustomApplicationm_application object
    containing information about an individual custom_appcustomApplicationlication"""
    return APICall("/customApplications")


@put
@payload_type(dict)
def update_custom_application(custom_application_id: ResourceID) -> APICall:
    """Updates and returns a customApplication object containing
    information about an individual customApplication"""
    url_path = f"/customApplications/{custom_application_id}"
    return APICall(url_path)


@delete
def delete_custom_application(custom_application_id: ResourceID) -> APICall:
    """Deletes a customApplication."""
    url_path = f"/customApplications/{custom_application_id}"
    return APICall(url_path)
