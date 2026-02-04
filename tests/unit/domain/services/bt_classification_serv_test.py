from uuid import uuid4

from domain.entities.business_type import BusinessType
from domain.services.business_type_class_service import (
    BusinessTypeClassificationService,
)
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId


def make_bt(name: str, parent=None):
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName(name),
        parent=parent,
    )


def test_get_all_descendants():
    root = make_bt("Root")
    child1 = make_bt("Child1", parent=root)
    child2 = make_bt("Child2", parent=root)
    grand = make_bt("Grand", parent=child1)

    result = BusinessTypeClassificationService.get_all_descendants(root)

    assert set(result) == {child1, child2, grand}


def test_get_all_ancestors():
    root = make_bt("Root")
    child = make_bt("Child", parent=root)
    grand = make_bt("Grand", parent=child)

    result = BusinessTypeClassificationService.get_all_ancestors(grand)

    assert result == [child, root]


def test_get_leaf_nodes():
    root = make_bt("Root")
    child1 = make_bt("Child1", parent=root)
    child2 = make_bt("Child2", parent=root)
    grand = make_bt("Grand", parent=child1)

    leaves = BusinessTypeClassificationService.get_leaf_nodes(root)

    assert set(leaves) == {child2, grand}
