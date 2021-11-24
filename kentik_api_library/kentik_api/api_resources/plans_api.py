from typing import List

from kentik_api.api_calls import plans
from kentik_api.api_resources.base_api import BaseAPI
from kentik_api.public.plan import Plan
from kentik_api.requests_payload import plans_payload


class PlansAPI(BaseAPI):
    """Exposes Kentik API operations related to plans."""

    def get_all(self) -> List[Plan]:
        api_call = plans.get_plans()
        response = self.send(api_call)
        return plans_payload.GetAllResponse.from_json(response.text).to_plans()
