import pytest
from application.use_cases.facilities.list_all_facilities import LitsAllFacilityUseCase
from conftest import make_facility
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository


@pytest.mark.asyncio
async def test_list_all_facilities():
    repo = InMemoryFacilityRepository()

    f1 = make_facility("A")
    f2 = make_facility("B")

    await repo.save(f1)
    await repo.save(f2)

    uc = LitsAllFacilityUseCase(repo)
    result = await uc.execute()

    assert set(result) == {f1, f2}
