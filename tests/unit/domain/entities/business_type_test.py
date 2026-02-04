import pytest
from uuid import uuid4

from domain.entities.business_type import BusinessType
from domain.val_objs.ids import BusinessTypeId
from domain.val_objs.business_name import BusinessName
from domain.exceptions.business_type_err import BusinessTypeHierarchyError



def test_create_root_business_type():
    bt = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )

    assert bt.parent is None
    assert bt.children == ()


def test_add_child():
    root = BusinessType(BusinessTypeId(uuid4()), BusinessName("Food"), None)
    child = BusinessType(BusinessTypeId(uuid4()), BusinessName("Meat"), root)

    assert child in root.children
    assert child.parent is root


def test_hierarchy_depth_limit():
    root = BusinessType(BusinessTypeId(uuid4()), BusinessName("Food"), None)
    lvl1 = BusinessType(BusinessTypeId(uuid4()), BusinessName("Meat"), root)
    lvl2 = BusinessType(BusinessTypeId(uuid4()), BusinessName("Beef"), lvl1)

    with pytest.raises(BusinessTypeHierarchyError):
        lvl3 = BusinessType(BusinessTypeId(uuid4()), BusinessName("Premium Beef"), lvl2)



def test_cannot_create_cycle():
    root = BusinessType(BusinessTypeId(uuid4()), BusinessName("Food"), None)
    child = BusinessType(BusinessTypeId(uuid4()), BusinessName("Meat"), root)

    with pytest.raises(BusinessTypeHierarchyError):
        child.add_child(root)


def test_children_are_immutable():
    root = BusinessType(BusinessTypeId(uuid4()), BusinessName("Food"), None)
    assert isinstance(root.children, tuple)


def test_remove_child():
    root = BusinessType(BusinessTypeId(uuid4()), BusinessName("Food"), None)
    child = BusinessType(BusinessTypeId(uuid4()), BusinessName("Meat"), root)

    root.remove_child(child)

    assert child not in root.children
    assert child.parent is None
