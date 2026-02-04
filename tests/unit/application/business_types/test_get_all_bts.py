from infra.repositories.in_mem_bt_repo import InMemoryBusinessTypeRepository
from application.use_cases.business_types.list_all_bt import ListAllBusinessTypesUseCase
import pytest

from conftest  import make_bt


@pytest.mark.asyncio
async def test_list_all_business_types():
    repo = InMemoryBusinessTypeRepository()

    bt1 = make_bt("Food")
    bt2 = make_bt("Tech")

    await repo.save(bt1)
    await repo.save(bt2)

    uc = ListAllBusinessTypesUseCase(repo)
    result = await uc.execute()

    assert set(result) == {bt1, bt2}
