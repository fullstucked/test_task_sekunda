import pytest
from application.use_cases.orgs.list_orgs_by_bt_rec import (
    ListOrganizationsByBusinessTypeRecursive,
)
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_list_orgs_by_bt_rec(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")

    root = make_bt("Root")
    child = make_bt("Child", parent=root)

    await fac_repo.save(fac)
    await bt_repo.save(root)
    await bt_repo.save(child)
    await db_session.commit()

    o1 = make_org("O1", fac, root)
    o2 = make_org("O2", fac, child)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    usecase = ListOrganizationsByBusinessTypeRecursive(org_repo)
    result = await usecase.execute(root.id)

    names = {o.name.value for o in result}
    assert names == {"O1", "O2"}
