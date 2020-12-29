from typing import List

from kentik_api.api_calls import batch
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.batch_operation import Criterion, Upsert, Deletion, BatchOperationPart
from kentik_api.requests_payload import batch_operations_payload


class BatchAPI(BaseAPI):
    """ Exposes Kentik API batch operations """

    def batch_operation_on_flow_tags(
        self, operation_part: BatchOperationPart
    ) -> batch_operations_payload.BatchResponse:
        apicall = batch.flow_tags_batch_operation()
        payload = self._get_payload(operation_part)
        response = self._send(apicall, payload)
        return batch_operations_payload.BatchResponse.from_json(response.text)

    def batch_operation_on_populators(
        self, dimension_name: str, operation_part: BatchOperationPart
    ) -> batch_operations_payload.BatchResponse:
        apicall = batch.populators_batch_operation(dimension_name)
        payload = self._get_payload(operation_part)
        response = self._send(apicall, payload)
        return batch_operations_payload.BatchResponse.from_json(response.text)

    def get_status(self, batch_operation_guid: str) -> batch_operations_payload.BatchStatusResponse:
        apicall = batch.get_batch_operation_status(batch_operation_guid)
        response = self._send(apicall)
        return batch_operations_payload.BatchStatusResponse.from_json(response.text)

    @staticmethod
    def _get_payload(operation_part: BatchOperationPart) -> batch_operations_payload.BatchRequest:
        return batch_operations_payload.BatchRequest(
            guid=operation_part.guid,
            replace_all=operation_part.replace_all,
            complete=operation_part.complete,
            upserts=[
                batch_operations_payload.BatchRequest.Upsert(
                    i.value,
                    [batch_operations_payload.BatchRequest.Upsert.Criterion(j.direction, j.addr) for j in i.criteria],
                )
                for i in operation_part.upserts
            ],
            deletes=[batch_operations_payload.BatchRequest.Delete(i.value) for i in operation_part.deletes],
        )
