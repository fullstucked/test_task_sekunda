from uuid import UUID

from domain.repositories.facility_repository import FacilityRepository
from domain.val_objs.ids import FacilityId


class GetFacilityByIdUseCase:
    def __init__(self, facility_repo: FacilityRepository):
        self._facility_repo = facility_repo

    async def execute(self, facility_id: UUID):
        facility_id_vo = FacilityId(facility_id)

        return await self._facility_repo.get_by_id(facility_id_vo)
