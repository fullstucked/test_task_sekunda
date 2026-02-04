import pytest
from application.use_cases.business_types.get_bt_by_id import GetBusinessTypeByIdUseCase
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl

from tests.integration.fixtures import make_bt


@pytest.mark.asyncio
async def test_get_bt_by_id(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)
    usecase = GetBusinessTypeByIdUseCase(repo)

    bt = make_bt("Food")
    await repo.save(bt)
    await db_session.commit()

    result = await usecase.execute(bt.id.value)

    assert result.id == bt.id
    assert result.name.value == "Food"
