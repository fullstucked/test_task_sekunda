import pytest
from application.use_cases.orgs.get_org_by_id import GetOrganizationByIdUseCase
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_get_org_by_id(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt = make_bt("Food")

    await fac_repo.save(fac)
    await bt_repo.save(bt)
    await db_session.commit()

    org = make_org("MyOrg", fac, bt)
    await org_repo.save(org)
    await db_session.commit()

    usecase = GetOrganizationByIdUseCase(org_repo)
    result = await usecase.execute(org.id.value)

    assert result.name.value == "MyOrg"
    assert result.facility.address.address == "HQ"
    assert result.business_types[0].name.value == "Food"
