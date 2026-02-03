from uuid import UUID

from domain.repositories.facility_repository import FacilityRepository
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import FacilityId


class ListOrganizationsByFacilityUseCase:
    def __init__(
        self, org_repo: OrganizationRepository, facility_repo: FacilityRepository
    ) -> None:
        self._org_repo = org_repo
        self._facility_repo = facility_repo

    async def execute(self, facility_id: UUID):
        facility_id_vo = FacilityId(facility_id)
        facility = await self._facility_repo.get_by_id(facility_id_vo)
        return await self._org_repo.list_by_facility(facility)
