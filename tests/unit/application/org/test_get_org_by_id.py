from uuid import uuid4

import pytest
from application.use_cases.orgs.get_org_by_id import GetOrganizationByIdUseCase
from conftest import make_bt, make_facility, make_org
from domain.exceptions.base import DomainResourceNotFoundError
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.mark.asyncio
async def test_get_org_by_id_success():
    repo = InMemoryOrganizationRepository()
    org = make_org("TestOrg", make_facility("A"), make_bt("Food"))
    await repo.save(org)

    uc = GetOrganizationByIdUseCase(repo)
    result = await uc.execute(org.id.value)

    assert result is org


@pytest.mark.asyncio
async def test_get_org_by_id_not_found():
    repo = InMemoryOrganizationRepository()
    uc = GetOrganizationByIdUseCase(repo)

    with pytest.raises(DomainResourceNotFoundError):
        await uc.execute(uuid4())
