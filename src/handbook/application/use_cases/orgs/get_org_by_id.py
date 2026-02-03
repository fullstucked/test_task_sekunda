from uuid import UUID

from domain.exceptions.base import DomainResourceNotFoundError
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import OrganizationId


class GetOrganizationByIdUseCase:
    def __init__(self, org_repo: OrganizationRepository) -> None:
        self._org_repo = org_repo

    async def execute(self, org_id: UUID):
        org_id_vo = OrganizationId(org_id)

        org = await self._org_repo.get_by_id(org_id_vo)
        if org is None:
            raise DomainResourceNotFoundError(
                "Organization not found",
                context={"organization_id": org_id},
            )
        return org
