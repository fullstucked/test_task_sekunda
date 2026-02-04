from uuid import UUID

from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.val_objs.ids import BusinessTypeId


class GetBusinessTypeByIdUseCase:
    def __init__(self, bt_repo: BusinessTypeRepository):
        self._bt_repo = bt_repo

    async def execute(self, bt_id: UUID):
        bt_id_vo = BusinessTypeId(bt_id)

        return await self._bt_repo.get_by_id(id=bt_id_vo)
