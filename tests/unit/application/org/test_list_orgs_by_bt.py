import pytest
from application.use_cases.orgs.list_orgs_by_bt import (
    ListOrganizationsByBusinessTypeUseCase,
)
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_bt_repo import InMemoryBusinessTypeRepository
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_list_orgs_by_business_type():
    org_repo = InMemoryOrganizationRepository()
    bt_repo = InMemoryBusinessTypeRepository()

    food = make_bt("Food")
    tech = make_bt("Tech")

    await bt_repo.save(food)
    await bt_repo.save(tech)

    org1 = make_org("FoodOrg", make_facility("A"), food)
    org2 = make_org("TechOrg", make_facility("A"), tech)

    await org_repo.save(org1)
    await org_repo.save(org2)

    uc = ListOrganizationsByBusinessTypeUseCase(org_repo, bt_repo)
    result = await uc.execute(food.id.value)

    assert set(result) == {org1}
