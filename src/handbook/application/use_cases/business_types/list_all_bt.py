from domain.repositories.business_type_repository import BusinessTypeRepository


class ListAllBusinessTypesUseCase:
    def __init__(self, bt_repo: BusinessTypeRepository):
        self._business_repo = bt_repo

    async def execute(self):
        return await self._business_repo.list_all()
