from kentik_api.api_calls import query_methods
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.requests_payload.queries_payload import GetDataResponse
from kentik_api.public.query_sql import SQLQuery, SQLQueryResult
from kentik_api.public.query_object import QueryObject, QueryResult


class QueryAPI(BaseAPI):
    """Exposes Kentik API's Query API methods"""

    def sql(self, query: SQLQuery) -> SQLQueryResult:
        apicall = query_methods.query_sql()
        payload = query
        response = self._send(apicall, payload)
        return SQLQueryResult.from_json(response.text)

    def data(self, query: QueryObject) -> QueryResult:
        apicall = query_methods.query_data()
        payload = query
        response = self._send(apicall, payload)
        return GetDataResponse.from_json(response.text).to_query_result()
