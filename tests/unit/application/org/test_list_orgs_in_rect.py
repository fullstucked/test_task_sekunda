from decimal import Decimal

import pytest
from application.use_cases.orgs.list_orgs_in_rect import (
    ListOrganizationsInRectangleUseCase,
)
from conftest import make_bt, make_facility, make_org
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_list_orgs_in_rectangle():
    org_repo = InMemoryOrganizationRepository()
    fac_repo = InMemoryFacilityRepository()

    f1 = make_facility("F1", lat="10", lon="10")
    f2 = make_facility("F2", lat="20", lon="20")
    f3 = make_facility("F3", lat="30", lon="30")

    await fac_repo.save(f1)
    await fac_repo.save(f2)
    await fac_repo.save(f3)

    org1 = make_org("Org1", f1, make_bt("Food"))
    org2 = make_org("Org2", f2, make_bt("Tech"))
    org3 = make_org("Org3", f3, make_bt("Meat"))

    await org_repo.save(org1)
    await org_repo.save(org2)
    await org_repo.save(org3)

    uc = ListOrganizationsInRectangleUseCase(org_repo, fac_repo)
    result = await uc.execute(
        Decimal("5"), Decimal("5"),
        Decimal("25"), Decimal("25")
    )

    assert set(result) == {org1, org2}
