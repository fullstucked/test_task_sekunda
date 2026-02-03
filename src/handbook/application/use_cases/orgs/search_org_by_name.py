from domain.repositories.organization_repository import OrganizationRepository


class SearchOrganizationByNameUseCase:
    def __init__(self, org_repo: OrganizationRepository) -> None:
        self._org_repo = org_repo

    async def execute(self, query: str):
        return list(await self._org_repo.search_by_name(query))
