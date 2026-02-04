from uuid import UUID

from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import OrganizationId


class GetOrganizationByIdUseCase:
    def __init__(self, org_repo: OrganizationRepository) -> None:
        self._org_repo = org_repo

    async def execute(self, org_id: UUID):
        org_id_vo = OrganizationId(org_id)
        return await self._org_repo.get_by_id(org_id_vo)
