from domain.repositories.facility_repository import FacilityRepository


class LitsAllFacilityUseCase:
    def __init__(self, facility_repo: FacilityRepository):
        self._facility_repo = facility_repo

    async def execute(self):
        return await self._facility_repo.list_all()
