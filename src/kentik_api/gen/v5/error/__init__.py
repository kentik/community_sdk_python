# AUTO-GENERATED: scripts/generation/error_package.py, generate_service_error_package()
# Rebuilt on every `uv run poe generate`. Do not edit by hand.

from __future__ import annotations

from typing import Any

from kentik_api.errors import HTTPException


class V5Error(HTTPException):
    """Base service-local error for the v5 API."""

    @classmethod
    def _build_error(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "V5Error":
        preview = getattr(response, "text", "")[:200].replace("\n", " ")
        headers = getattr(response, "headers", {})
        content_type = (
            headers.get("content-type", "unknown")
            if hasattr(headers, "get")
            else "unknown"
        )
        details: dict[str, Any] = {
            "content_type": content_type,
            "preview": preview,
        }
        message = f"{operation_name} failed with status code: {getattr(response, 'status_code', 'unknown')}"
        try:
            payload = response.json()
        except Exception:
            payload = None
        if isinstance(payload, dict):
            details["response_json"] = payload
            if isinstance(payload.get("error"), str) and payload["error"]:
                message = f"{message}: {payload['error']}"
            message = payload.get("message") or message
        elif payload is not None:
            details["response_json"] = payload
        return cls(
            getattr(response, "status_code", 500),
            message,
            method=method,
            path=path,
            details=details,
        )

    @classmethod
    def from_response(
        cls, response: Any, *, operation_name: str, method: str, path: str
    ) -> "V5Error":
        status_key = str(getattr(response, "status_code", ""))
        response_error_map = getattr(cls, "response_error_map", {})
        target_cls = (
            response_error_map.get(status_key)
            or response_error_map.get("default")
            or cls
        )
        return target_cls._build_error(
            response,
            operation_name=operation_name,
            method=method,
            path=path,
        )


class BatchPopulatorsError(V5Error):
    """Operation-local error for client.v5.batch_populators()."""

    response_error_map: dict[str, type[V5Error]] = {}


class BatchPopulatorsBadRequestError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class BatchPopulatorsUnauthorizedError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class BatchPopulatorsForbiddenError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class BatchPopulatorsNotFoundError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class BatchPopulatorsTooManyRequestsError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class BatchPopulatorsInternalServerErrorError(BatchPopulatorsError):
    """Operation-local response error for batch_populators (500: The API failed. #/components/schemas/V5Error)."""

    pass


BatchPopulatorsError.response_error_map = {
    "400": BatchPopulatorsBadRequestError,
    "401": BatchPopulatorsUnauthorizedError,
    "403": BatchPopulatorsForbiddenError,
    "404": BatchPopulatorsNotFoundError,
    "429": BatchPopulatorsTooManyRequestsError,
    "500": BatchPopulatorsInternalServerErrorError,
}


class BatchStatusError(V5Error):
    """Operation-local error for client.v5.batch_status()."""

    response_error_map: dict[str, type[V5Error]] = {}


class BatchStatusBadRequestError(BatchStatusError):
    """Operation-local response error for batch_status (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class BatchStatusUnauthorizedError(BatchStatusError):
    """Operation-local response error for batch_status (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class BatchStatusForbiddenError(BatchStatusError):
    """Operation-local response error for batch_status (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class BatchStatusNotFoundError(BatchStatusError):
    """Operation-local response error for batch_status (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class BatchStatusTooManyRequestsError(BatchStatusError):
    """Operation-local response error for batch_status (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class BatchStatusInternalServerErrorError(BatchStatusError):
    """Operation-local response error for batch_status (500: The API failed. #/components/schemas/V5Error)."""

    pass


BatchStatusError.response_error_map = {
    "400": BatchStatusBadRequestError,
    "401": BatchStatusUnauthorizedError,
    "403": BatchStatusForbiddenError,
    "404": BatchStatusNotFoundError,
    "429": BatchStatusTooManyRequestsError,
    "500": BatchStatusInternalServerErrorError,
}


class BatchTagsError(V5Error):
    """Operation-local error for client.v5.batch_tags()."""

    response_error_map: dict[str, type[V5Error]] = {}


class BatchTagsBadRequestError(BatchTagsError):
    """Operation-local response error for batch_tags (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class BatchTagsUnauthorizedError(BatchTagsError):
    """Operation-local response error for batch_tags (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class BatchTagsForbiddenError(BatchTagsError):
    """Operation-local response error for batch_tags (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class BatchTagsNotFoundError(BatchTagsError):
    """Operation-local response error for batch_tags (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class BatchTagsTooManyRequestsError(BatchTagsError):
    """Operation-local response error for batch_tags (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class BatchTagsInternalServerErrorError(BatchTagsError):
    """Operation-local response error for batch_tags (500: The API failed. #/components/schemas/V5Error)."""

    pass


BatchTagsError.response_error_map = {
    "400": BatchTagsBadRequestError,
    "401": BatchTagsUnauthorizedError,
    "403": BatchTagsForbiddenError,
    "404": BatchTagsNotFoundError,
    "429": BatchTagsTooManyRequestsError,
    "500": BatchTagsInternalServerErrorError,
}


class QueryUrlError(V5Error):
    """Operation-local error for client.v5.query_url()."""

    response_error_map: dict[str, type[V5Error]] = {}


class QueryUrlBadRequestError(QueryUrlError):
    """Operation-local response error for query_url (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class QueryUrlUnauthorizedError(QueryUrlError):
    """Operation-local response error for query_url (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class QueryUrlForbiddenError(QueryUrlError):
    """Operation-local response error for query_url (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class QueryUrlNotFoundError(QueryUrlError):
    """Operation-local response error for query_url (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class QueryUrlTooManyRequestsError(QueryUrlError):
    """Operation-local response error for query_url (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class QueryUrlInternalServerErrorError(QueryUrlError):
    """Operation-local response error for query_url (500: The API failed. #/components/schemas/V5Error)."""

    pass


QueryUrlError.response_error_map = {
    "400": QueryUrlBadRequestError,
    "401": QueryUrlUnauthorizedError,
    "403": QueryUrlForbiddenError,
    "404": QueryUrlNotFoundError,
    "429": QueryUrlTooManyRequestsError,
    "500": QueryUrlInternalServerErrorError,
}


class TopXChartError(V5Error):
    """Operation-local error for client.v5.top_x_chart()."""

    response_error_map: dict[str, type[V5Error]] = {}


class TopXChartBadRequestError(TopXChartError):
    """Operation-local response error for top_x_chart (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class TopXChartUnauthorizedError(TopXChartError):
    """Operation-local response error for top_x_chart (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class TopXChartForbiddenError(TopXChartError):
    """Operation-local response error for top_x_chart (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class TopXChartNotFoundError(TopXChartError):
    """Operation-local response error for top_x_chart (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class TopXChartTooManyRequestsError(TopXChartError):
    """Operation-local response error for top_x_chart (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class TopXChartInternalServerErrorError(TopXChartError):
    """Operation-local response error for top_x_chart (500: The API failed. #/components/schemas/V5Error)."""

    pass


TopXChartError.response_error_map = {
    "400": TopXChartBadRequestError,
    "401": TopXChartUnauthorizedError,
    "403": TopXChartForbiddenError,
    "404": TopXChartNotFoundError,
    "429": TopXChartTooManyRequestsError,
    "500": TopXChartInternalServerErrorError,
}


class TopXDataError(V5Error):
    """Operation-local error for client.v5.top_x_data()."""

    response_error_map: dict[str, type[V5Error]] = {}


class TopXDataBadRequestError(TopXDataError):
    """Operation-local response error for top_x_data (400: The request is not valid, for example a query without device_name. #/components/schemas/V5Error)."""

    pass


class TopXDataUnauthorizedError(TopXDataError):
    """Operation-local response error for top_x_data (401: The credentials are missing or wrong. #/components/schemas/V5Error)."""

    pass


class TopXDataForbiddenError(TopXDataError):
    """Operation-local response error for top_x_data (403: The user may not call this endpoint. #/components/schemas/V5Error)."""

    pass


class TopXDataNotFoundError(TopXDataError):
    """Operation-local response error for top_x_data (404: The resource does not exist. #/components/schemas/V5Error)."""

    pass


class TopXDataTooManyRequestsError(TopXDataError):
    """Operation-local response error for top_x_data (429: The rate limit is exceeded. V5 sends no rate limit headers. #/components/schemas/V5Error)."""

    pass


class TopXDataInternalServerErrorError(TopXDataError):
    """Operation-local response error for top_x_data (500: The API failed. #/components/schemas/V5Error)."""

    pass


TopXDataError.response_error_map = {
    "400": TopXDataBadRequestError,
    "401": TopXDataUnauthorizedError,
    "403": TopXDataForbiddenError,
    "404": TopXDataNotFoundError,
    "429": TopXDataTooManyRequestsError,
    "500": TopXDataInternalServerErrorError,
}

ERROR_BY_METHOD: dict[str, type[V5Error]] = {
    "batch_populators": BatchPopulatorsError,
    "batch_status": BatchStatusError,
    "batch_tags": BatchTagsError,
    "query_url": QueryUrlError,
    "top_x_chart": TopXChartError,
    "top_x_data": TopXDataError,
}

__all__ = [
    "V5Error",
    "BatchPopulatorsBadRequestError",
    "BatchPopulatorsUnauthorizedError",
    "BatchPopulatorsForbiddenError",
    "BatchPopulatorsNotFoundError",
    "BatchPopulatorsTooManyRequestsError",
    "BatchPopulatorsInternalServerErrorError",
    "BatchStatusBadRequestError",
    "BatchStatusUnauthorizedError",
    "BatchStatusForbiddenError",
    "BatchStatusNotFoundError",
    "BatchStatusTooManyRequestsError",
    "BatchStatusInternalServerErrorError",
    "BatchTagsBadRequestError",
    "BatchTagsUnauthorizedError",
    "BatchTagsForbiddenError",
    "BatchTagsNotFoundError",
    "BatchTagsTooManyRequestsError",
    "BatchTagsInternalServerErrorError",
    "QueryUrlBadRequestError",
    "QueryUrlUnauthorizedError",
    "QueryUrlForbiddenError",
    "QueryUrlNotFoundError",
    "QueryUrlTooManyRequestsError",
    "QueryUrlInternalServerErrorError",
    "TopXChartBadRequestError",
    "TopXChartUnauthorizedError",
    "TopXChartForbiddenError",
    "TopXChartNotFoundError",
    "TopXChartTooManyRequestsError",
    "TopXChartInternalServerErrorError",
    "TopXDataBadRequestError",
    "TopXDataUnauthorizedError",
    "TopXDataForbiddenError",
    "TopXDataNotFoundError",
    "TopXDataTooManyRequestsError",
    "TopXDataInternalServerErrorError",
    "BatchPopulatorsError",
    "BatchStatusError",
    "BatchTagsError",
    "QueryUrlError",
    "TopXChartError",
    "TopXDataError",
    "ERROR_BY_METHOD",
]
