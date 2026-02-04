import pytest
from application.use_cases.business_types.list_all_bt import ListAllBusinessTypesUseCase
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl

from tests.integration.fixtures import make_bt


@pytest.mark.asyncio
async def test_list_all_bt(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)
    usecase = ListAllBusinessTypesUseCase(repo)

    a = make_bt("AAAA")
    b = make_bt("BBBB")

    await repo.save(a)
    await repo.save(b)
    await db_session.commit()

    result = await usecase.execute()

    names = {bt.name.value for bt in result}
    assert names == {"AAAA", "BBBB"}
