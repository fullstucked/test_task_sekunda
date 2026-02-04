import pytest
from application.use_cases.orgs.search_org_by_name import SearchOrganizationsByName
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_search_org_by_name(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt = make_bt("Food")

    await fac_repo.save(fac)
    await bt_repo.save(bt)
    await db_session.commit()

    o1 = make_org("Coffee House", fac, bt)
    o2 = make_org("Tech Hub", fac, bt)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    usecase = SearchOrganizationsByName(org_repo)
    result = await usecase.execute("coffee")

    names = {o.name.value for o in result}
    assert names == {"Coffee House"}
