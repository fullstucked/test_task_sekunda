import pytest
from application.use_cases.orgs.list_orgs_by_facility import ListOrganizationsByFacility
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_list_orgs_by_facility(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac1 = make_facility("A")
    fac2 = make_facility("B")
    bt = make_bt("Food")

    await fac_repo.save(fac1)
    await fac_repo.save(fac2)
    await bt_repo.save(bt)
    await db_session.commit()

    o1 = make_org("O1", fac1, bt)
    o2 = make_org("O2", fac1, bt)
    o3 = make_org("O3", fac2, bt)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await org_repo.save(o3)
    await db_session.commit()

    usecase = ListOrganizationsByFacility(org_repo)
    result = await usecase.execute(fac1.id)

    names = {o.name.value for o in result}
    assert names == {"O1", "O2"}
