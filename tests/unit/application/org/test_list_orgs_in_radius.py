from decimal import Decimal

import pytest
from application.use_cases.orgs.list_orgs_by_rad import ListOrganizationsInRadiusUseCase
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_list_orgs_in_radius():
    org_repo = InMemoryOrganizationRepository()
    fac_repo = InMemoryFacilityRepository()

    near = make_facility("Near", lat="0.001", lon="0.001")
    far = make_facility("Far", lat="1", lon="1")

    await fac_repo.save(near)
    await fac_repo.save(far)

    org1 = make_org("NearOrg", near, make_bt("Food"))
    org2 = make_org("FarOrg", far, make_bt("Tech"))

    await org_repo.save(org1)
    await org_repo.save(org2)

    uc = ListOrganizationsInRadiusUseCase(fac_repo, org_repo)
    result = await uc.execute(Decimal("0"), Decimal("0"), 500)

    assert result == [org1]
