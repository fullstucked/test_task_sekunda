from decimal import Decimal

from domain.repositories.facility_repository import FacilityRepository
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.coords import Coordinates


class ListOrganizationsInRadiusUseCase:
    def __init__(
        self,
        facility_repo: FacilityRepository,
        org_repo: OrganizationRepository,
    ) -> None:
        self._facility_repo = facility_repo
        self._org_repo = org_repo

    async def execute(self, lat: Decimal, lon: Decimal, radius_meters: float):
        center = Coordinates(lat=lat, lon=lon)
        facilities = await self._facility_repo.list_in_radius(center, radius_meters)

        orgs: list = []
        for facility in facilities:
            orgs.extend(await self._org_repo.list_by_facility(facility))

        return orgs
