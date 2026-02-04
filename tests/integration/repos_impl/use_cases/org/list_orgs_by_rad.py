import pytest
from application.use_cases.orgs.list_orgs_by_rad import ListOrganizationsByRadius
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_list_orgs_by_rad(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    center = make_facility("Center", lat="10", lon="20")
    near = make_facility("Near", lat="10.0001", lon="20.0001")
    far = make_facility("Far", lat="50", lon="50")

    bt = make_bt("Food")

    await fac_repo.save(center)
    await fac_repo.save(near)
    await fac_repo.save(far)
    await bt_repo.save(bt)
    await db_session.commit()

    o1 = make_org("NearOrg", near, bt)
    o2 = make_org("FarOrg", far, bt)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    usecase = ListOrganizationsByRadius(org_repo)
    result = await usecase.execute(center.coordinates, 500)

    names = {o.name.value for o in result}
    assert "NearOrg" in names
    assert "FarOrg" not in names
