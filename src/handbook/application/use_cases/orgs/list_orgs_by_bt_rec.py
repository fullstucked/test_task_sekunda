from typing import Iterable
from uuid import UUID

from domain.entities.organization import Organization
from domain.exceptions.base import DomainBusinessRuleError
from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.repositories.organization_repository import OrganizationRepository
from domain.services.business_type_class_service import (
    BusinessTypeClassificationService,
)
from domain.val_objs.ids import BusinessTypeId


class ListOrganizationsByBusinessTypeRecursiveUseCase:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        bt_repo: BusinessTypeRepository,
    ) -> None:
        self._org_repo = org_repo
        self._bt_repo = bt_repo

    async def execute(self, root_bt_id: UUID) -> Iterable[Organization]:
        root_bt_vo_id = BusinessTypeId(root_bt_id)
        root_bt = await self._bt_repo.get_by_id(root_bt_vo_id)

        if root_bt is None:
            raise DomainBusinessRuleError(
                f"BusinessType with id {root_bt_id} does not exist"
            )

        descendants = await BusinessTypeClassificationService.get_all_descendants(
            root_bt
        )

        all_descendants = [root_bt] + descendants
        result = await self._org_repo.list_by_business_types(all_descendants)
        return result
