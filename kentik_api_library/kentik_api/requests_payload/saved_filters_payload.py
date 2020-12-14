from dataclasses import dataclass
import json
from typing import Optional, Dict, List

from kentik_api.public.saved_filter import SavedFilter, Filters, FilterGroups, Filter


@dataclass()
class GetResponse:
    id: Optional[int] = None,
    company_id: Optional[int] = None,
    filters: Optional[Dict] = None,
    filter_name: Optional[str] = None,
    filter_description: Optional[str] = None,
    cdate: Optional[str] = None,
    edate: Optional[str] = None,
    filter_level: Optional[str] = None,

    @classmethod
    def from_json(cls, json_string):
        dic = json.loads(json_string)
        return cls(**dic)

    def to_saved_filter(self, dic) ->SavedFilter:
        return SavedFilter

    def _to_filters(self, dic) ->Filters:
        pass

    def _to_filtergroups(self, dic) ->FilterGroups:
        pass

    def _to_filter(self, dic) ->Filter:
        pass
