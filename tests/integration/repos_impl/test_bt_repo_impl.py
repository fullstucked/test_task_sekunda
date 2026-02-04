import pytest
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl

from tests.integration.fixtures import make_bt


@pytest.mark.asyncio
async def test_bt_save_and_get(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    root = make_bt("Root")
    await repo.save(root)
    await db_session.commit()

    loaded = await repo.get_by_id(root.id)
    assert loaded.id == root.id
    assert loaded.name.value == "Root"


@pytest.mark.asyncio
async def test_bt_get_by_name(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    bt = make_bt("Coffee")
    await repo.save(bt)
    await db_session.commit()

    loaded = await repo.get_by_name(bt.name)
    assert loaded.name.value == "Coffee"


@pytest.mark.asyncio
async def test_bt_list_all(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    a = make_bt("AAAA")
    b = make_bt("BBBB")
    await repo.save(a)
    await repo.save(b)
    await db_session.commit()

    result = await repo.list_all()
    names = {bt.name.value for bt in result}

    assert names == {"AAAA", "BBBB"}


@pytest.mark.asyncio
async def test_bt_children_and_roots(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    root = make_bt("Root")
    child1 = make_bt("Child1", parent=root)
    child2 = make_bt("Child2", parent=root)

    await repo.save(root)
    await repo.save(child1)
    await repo.save(child2)
    await db_session.commit()

    roots = await repo.list_roots()
    assert len(roots) == 1
    assert roots[0].name.value == "Root"

    children = await repo.list_children(root)
    names = {c.name.value for c in children}
    assert names == {"Child1", "Child2"}


@pytest.mark.asyncio
async def test_bt_descendants(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    root = make_bt("Root")
    c1 = make_bt("C1aa", parent=root)
    c2 = make_bt("C2aa", parent=c1)

    await repo.save(root)
    await repo.save(c1)
    await repo.save(c2)
    await db_session.commit()

    descendants = await repo.list_descendants(root)
    names = {d.name.value for d in descendants}

    assert names == {"C1aa", "C2aa"}


@pytest.mark.asyncio
async def test_bt_delete(db_session):
    repo = BusinessTypeRepositoryImpl(db_session)

    bt = make_bt("DeleteMe")
    await repo.save(bt)
    await db_session.commit()

    await repo.delete(bt)
    await db_session.commit()

    with pytest.raises(Exception):
        await repo.get_by_id(bt.id)
