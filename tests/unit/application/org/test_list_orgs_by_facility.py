import pytest
from application.use_cases.orgs.list_orgs_by_facility import (
    ListOrganizationsByFacilityUseCase,
)
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_list_orgs_by_facility():
    org_repo = InMemoryOrganizationRepository()
    fac_repo = InMemoryFacilityRepository()

    fac1 = make_facility("A")
    fac2 = make_facility("B")

    await fac_repo.save(fac1)
    await fac_repo.save(fac2)

    org1 = make_org("Org1", fac1, make_bt("Food"))
    org2 = make_org("Org2", fac2, make_bt("Tech"))

    await org_repo.save(org1)
    await org_repo.save(org2)

    uc = ListOrganizationsByFacilityUseCase(org_repo, fac_repo)
    result = await uc.execute(fac1.id.value)

    assert result == [org1]
