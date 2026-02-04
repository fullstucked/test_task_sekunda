from infra.repositories.in_mem_bt_repo import InMemoryBusinessTypeRepository
from application.use_cases.business_types.get_bt_by_id import GetBusinessTypeByIdUseCase
import pytest
from uuid import uuid4

from conftest  import make_bt
from domain.exceptions.base import DomainResourceNotFoundError


@pytest.mark.asyncio
async def test_get_business_type_by_id_success():
    repo = InMemoryBusinessTypeRepository()
    bt = make_bt("Food")
    await repo.save(bt)

    uc = GetBusinessTypeByIdUseCase(repo)
    result = await uc.execute(bt.id.value)

    assert result is bt


@pytest.mark.asyncio
async def test_get_business_type_by_id_not_found():
    repo = InMemoryBusinessTypeRepository()
    uc = GetBusinessTypeByIdUseCase(repo)

    with pytest.raises(DomainResourceNotFoundError):
        await uc.execute(uuid4())
