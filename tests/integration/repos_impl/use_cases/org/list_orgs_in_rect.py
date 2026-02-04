import pytest
from application.use_cases.orgs.list_orgs_in_rect import ListOrganizationsInRectangle
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_list_orgs_in_rect(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    inside = make_facility("Inside", lat="10", lon="20")
    outside = make_facility("Outside", lat="50", lon="50")
    bt = make_bt("Food")

    await fac_repo.save(inside)
    await fac_repo.save(outside)
    await bt_repo.save(bt)
    await db_session.commit()

    o1 = make_org("InsideOrg", inside, bt)
    o2 = make_org("OutsideOrg", outside, bt)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    usecase = ListOrganizationsInRectangle(org_repo)
    result = await usecase.execute(
        inside.coordinates,
        make_facility(lat="11", lon="21").coordinates,
    )

    names = {o.name.value for o in result}
    assert names == {"InsideOrg"}

