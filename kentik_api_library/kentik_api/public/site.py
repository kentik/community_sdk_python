from typing import Optional


class Site:
    def __init__(
        self,
        site_name: Optional[str] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        id: Optional[int] = None,
        company_id: Optional[str] = None,
    ) -> None:
        # read-write
        self.site_name = site_name
        self.latitude = latitude
        self.longitude = longitude

        # read-only
        self._id = id
        self._company_id = company_id

    @property
    def id(self) -> int:
        assert self._id is not None
        return self._id

    @property
    def company_id(self) -> Optional[str]:
        return self._company_id
