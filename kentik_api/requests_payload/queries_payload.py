from base64 import b64decode
from dataclasses import dataclass
from typing import Dict, List, Tuple

from kentik_api.public.query_object import ImageType, QueryChartResult, QueryDataResult, QueryURLResult
from kentik_api.requests_payload.conversions import dict_from_json, from_dict


@dataclass
class QueryURLResponse:
    received_url: str

    def to_query_url_result(self) -> QueryURLResult:
        unquoted_url = self.received_url[1:-1]  # received url is in quotation marks
        return QueryURLResult(url=unquoted_url)


@dataclass()
class QueryDataResponse:
    results: List[Dict]

    @classmethod
    def from_json(cls, json_string: str):
        params = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, params)

    def to_query_data_result(self) -> QueryDataResult:
        return QueryDataResult(results=self.results)


@dataclass
class QueryChartResponse:
    dataUri: str  # like: "data:image/png;base64,iVBORw0KGgoAAAA..."

    @classmethod
    def from_json(cls, json_string: str):
        params = dict_from_json(cls.__name__, json_string)
        return from_dict(cls, params)

    def to_query_chart_result(self) -> QueryChartResult:
        data = str.encode(self._get_image_data_base64())
        return QueryChartResult(image_type=self._get_image_type(), image_data=b64decode(data))

    def _get_image_type(self) -> ImageType:
        mime_type, _, _ = _parse_uri(self.dataUri)
        if mime_type == "image/png":
            return ImageType.png
        if mime_type == "image/jpeg":
            return ImageType.jpg
        if mime_type == "image/svg+xml":
            return ImageType.svg
        if mime_type == "application/pdf":
            return ImageType.pdf
        raise ValueError(f"Expected mime type png/jpeg/svg/pdf, got: {mime_type}")

    def _get_image_data_base64(self) -> str:
        _, data_encoding, payload = _parse_uri(self.dataUri)
        if data_encoding != "base64":
            raise ValueError(f"Expected base64 encoding, got: {data_encoding}")
        return payload


def _parse_uri(uri_string: str) -> Tuple[str, str, str]:
    """Returns: (mime type, encoding type, payload data)"""
    uri = uri_string  # eg. "data:image/png;base64,iVBORw0KGgoAAAA..."
    data_type, uri = _cut_head(uri, ":")
    mime_type, uri = _cut_head(uri, ";")
    encoding_type, uri = _cut_head(uri, ",")
    payload = uri
    if data_type != "data" or mime_type == "" or encoding_type == "" or payload == "":
        raise ValueError(f"Invalid URI: {uri_string[:50]}")
    return (mime_type, encoding_type, payload)


def _cut_head(string: str, until: str) -> Tuple[str, str]:
    pos = string.find(until)
    if pos == -1:
        return ("", string)
    return (string[:pos], string[pos + 1 :])
