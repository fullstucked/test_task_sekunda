from decimal import Decimal

from domain.repositories.facility_repository import FacilityRepository
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.coords import Coordinates


class ListOrganizationsInRectangleUseCase:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        facility_repo: FacilityRepository,
    ) -> None:
        self.org_repo = org_repo
        self.facility_repo = facility_repo

    async def execute(
        self,
        lat1: Decimal,
        lon1: Decimal,
        lat2: Decimal,
        lon2: Decimal,
    ):
        p1 = Coordinates(lat=lat1, lon=lon1)
        p2 = Coordinates(lat=lat2, lon=lon2)

        facilities = await self.facility_repo.list_in_rectangle(p1=p1, p2=p2)

        orgs = []
        for facility in facilities:
            orgs.extend(await self.org_repo.list_by_facility(facility))

        return orgs
