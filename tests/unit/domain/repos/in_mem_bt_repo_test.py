from uuid import uuid4

import pytest
from domain.entities.business_type import BusinessType
from domain.exceptions.base import DomainResourceNotFoundError
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId
from infra.repositories.in_mem_bt_repo import InMemoryBusinessTypeRepository


@pytest.fixture
def repo():
    return InMemoryBusinessTypeRepository()


def make_bt(name: str, parent=None):
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName(name),
        parent=parent,
    )


# ---------------------------------------------------------
# CRUD
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_save_and_get_by_id(repo):
    bt = make_bt("Food")
    await repo.save(bt)

    loaded = await repo.get_by_id(bt.id)
    assert loaded is bt


@pytest.mark.asyncio
async def test_get_by_id_not_found(repo):
    with pytest.raises(DomainResourceNotFoundError):
        await repo.get_by_id(BusinessTypeId(uuid4()))


@pytest.mark.asyncio
async def test_get_by_name(repo):
    bt = make_bt("Tech")
    await repo.save(bt)

    loaded = await repo.get_by_name(BusinessName("Tech"))
    assert loaded is bt


@pytest.mark.asyncio
async def test_get_by_name_not_found(repo):
    with pytest.raises(DomainResourceNotFoundError):
        await repo.get_by_name(BusinessName("Unknown"))


@pytest.mark.asyncio
async def test_list_all(repo):
    bt1 = make_bt("AAAA")
    bt2 = make_bt("BBBB")

    await repo.save(bt1)
    await repo.save(bt2)

    result = await repo.list_all()
    assert set(result) == {bt1, bt2}


@pytest.mark.asyncio
async def test_delete(repo):
    bt = make_bt("DeleteMe")
    await repo.save(bt)
    await repo.delete(bt)

    with pytest.raises(DomainResourceNotFoundError):
        await repo.get_by_id(bt.id)


# ---------------------------------------------------------
# Hierarchy-specific queries
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_list_children(repo):
    root = make_bt("Root")
    child1 = make_bt("Child1", parent=root)
    child2 = make_bt("Child2", parent=root)

    await repo.save(root)
    await repo.save(child1)
    await repo.save(child2)

    result = await repo.list_children(root)
    assert set(result) == {child1, child2}


@pytest.mark.asyncio
async def test_list_roots(repo):
    root1 = make_bt("Root1")
    root2 = make_bt("Root2")
    child = make_bt("Child", parent=root1)

    await repo.save(root1)
    await repo.save(root2)
    await repo.save(child)

    result = await repo.list_roots()
    assert set(result) == {root1, root2}


@pytest.mark.asyncio
async def test_list_descendants(repo):
    root = make_bt("Root")
    child = make_bt("Child", parent=root)
    grand = make_bt("Grand", parent=child)

    await repo.save(root)
    await repo.save(child)
    await repo.save(grand)

    result = await repo.list_descendants(root)
    assert set(result) == {child, grand}
