from kentik_api.api_calls import query_methods
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.query import SQLQuery, SQLQueryResult


class QueryAPI(BaseAPI):
    """Exposes Kentik API's Query API methods"""

    def sql(self, query: SQLQuery) -> SQLQueryResult:
        apicall = query_methods.query_sql()
        payload = query
        response = self._send(apicall, payload)
        return SQLQueryResult.from_json(response.text)
