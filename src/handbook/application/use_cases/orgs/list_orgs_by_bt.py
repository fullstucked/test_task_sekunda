from typing import Iterable
from uuid import UUID

from domain.entities.organization import Organization
from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import BusinessTypeId


class ListOrganizationsByBusinessTypeUseCase:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        bt_repo: BusinessTypeRepository,
    ) -> None:
        self._org_repo = org_repo
        self._bt_repo = bt_repo

    async def execute(self, bt_id: UUID) -> Iterable[Organization]:
        bt_vo_id = BusinessTypeId(bt_id)
        bt = await self._bt_repo.get_by_id(bt_vo_id)
        if bt is None:
            raise ValueError(f"BusinessType {bt_id} does not exist")

        return await self._org_repo.list_by_business_type(bt)
