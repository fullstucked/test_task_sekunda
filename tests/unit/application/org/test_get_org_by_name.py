import pytest
from application.use_cases.orgs.search_org_by_name import (
    SearchOrganizationByNameUseCase,
)
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_search_org_by_name():
    repo = InMemoryOrganizationRepository()

    org1 = make_org("Alpha", make_facility("A"), make_bt("Food"))
    org2 = make_org("Beta", make_facility("A"), make_bt("Tech"))

    await repo.save(org1)
    await repo.save(org2)

    uc = SearchOrganizationByNameUseCase(repo)
    result = await uc.execute("alp")

    assert result == [org1]
