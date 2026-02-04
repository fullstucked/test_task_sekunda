import pytest
from application.use_cases.facilities.list_all_facilities import LitsAllFacilityUseCase
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl

from tests.integration.fixtures import make_facility


@pytest.mark.asyncio
async def test_list_all_facilities(db_session):
    repo = FacilityRepositoryImpl(db_session)
    usecase = LitsAllFacilityUseCase(repo)

    f1 = make_facility("A")
    f2 = make_facility("B")

    await repo.save(f1)
    await repo.save(f2)
    await db_session.commit()

    result = await usecase.execute()

    names = {f.address.address for f in result}
    assert names == {"A", "B"}
