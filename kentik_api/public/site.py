from typing import Optional

from kentik_api.public.errors import IncompleteObjectError
from kentik_api.public.types import ID


class Site:
    # pylint: disable=too-many-arguments
    def __init__(
        self,
        site_name: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        id: Optional[ID] = None,
        company_id: Optional[ID] = None,
    ) -> None:
        # read-write
        self.site_name = site_name
        self.latitude = latitude
        self.longitude = longitude

        # read-only
        self._id = id
        self._company_id = company_id

    # pylint: enable=too-many-arguments

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IncompleteObjectError("", self.__class__.__name__, "_id is required")
        return self._id

    @property
    def company_id(self) -> Optional[ID]:
        return self._company_id
