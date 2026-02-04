import pytest
from application.use_cases.orgs.list_orgs_by_bt_rec import (
    ListOrganizationsByBusinessTypeRecursiveUseCase,
)
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_bt_repo import InMemoryBusinessTypeRepository
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_list_orgs_by_business_type_recursive():
    org_repo = InMemoryOrganizationRepository()
    bt_repo = InMemoryBusinessTypeRepository()

    root = make_bt("Food")
    child = make_bt("Meat", parent=root)
    await bt_repo.save(root)
    await bt_repo.save(child)

    org1 = make_org("RootOrg", make_facility("A"), root)
    org2 = make_org("ChildOrg", make_facility("A"), child)

    await org_repo.save(org1)
    await org_repo.save(org2)

    uc = ListOrganizationsByBusinessTypeRecursiveUseCase(org_repo, bt_repo)
    result = await uc.execute(root.id.value)

    assert set(result) == {org1, org2}
