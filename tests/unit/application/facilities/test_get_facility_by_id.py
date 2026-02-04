from uuid import uuid4

import pytest
from application.use_cases.facilities.get_facility_by_id import GetFacilityByIdUseCase
from conftest import make_facility
from domain.exceptions.base import DomainResourceNotFoundError
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository


@pytest.mark.asyncio
async def test_get_facility_by_id_success():
    repo = InMemoryFacilityRepository()
    fac = make_facility("A")
    await repo.save(fac)

    uc = GetFacilityByIdUseCase(repo)
    result = await uc.execute(fac.id.value)

    assert result is fac


@pytest.mark.asyncio
async def test_get_facility_by_id_not_found():
    repo = InMemoryFacilityRepository()
    uc = GetFacilityByIdUseCase(repo)

    with pytest.raises(DomainResourceNotFoundError):
        await uc.execute(uuid4())
