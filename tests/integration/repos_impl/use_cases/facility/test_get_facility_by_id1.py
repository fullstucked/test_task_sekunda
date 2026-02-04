import pytest
from application.use_cases.facilities.get_facility_by_id import GetFacilityByIdUseCase
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl

from tests.integration.fixtures import make_facility


@pytest.mark.asyncio
async def test_get_facility_by_id(db_session):
    repo = FacilityRepositoryImpl(db_session)
    usecase = GetFacilityByIdUseCase(repo)

    fac = make_facility("HQ")
    await repo.save(fac)
    await db_session.commit()

    result = await usecase.execute(fac.id.value)

    assert result.id == fac.id
    assert result.address.address == "HQ"
