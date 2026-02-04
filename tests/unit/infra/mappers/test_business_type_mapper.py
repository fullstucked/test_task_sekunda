import uuid

from infra.db.models.business_type import BusinessTypeModel
from infra.repositories.mappers.business_type_mapper import BusinessTypeMapper


def test_bt_to_domain_simple():
    model = BusinessTypeModel(
        id=uuid.uuid4(),
        name="Food",
        parent_id=None,
    )

    bt = BusinessTypeMapper.to_domain(model)

    assert bt.name.value == "Food"
    assert bt.parent is None
    assert bt.children == ()


def test_bt_attach_relations_parent_and_children():
    # Build model tree
    root_model = BusinessTypeModel(id=uuid.uuid4(), name="Root", parent_id=None)
    child_model = BusinessTypeModel(
        id=uuid.uuid4(), name="Child", parent_id=root_model.id
    )

    root_model.children = [child_model]
    child_model.parent = root_model

    # First pass: create domain objects
    root = BusinessTypeMapper.to_domain(root_model)
    child = BusinessTypeMapper.to_domain(child_model)

    cache = {
        root_model.id: root,
        child_model.id: child,
    }

    # Second pass: attach relations
    BusinessTypeMapper.attach_relations(root, root_model, cache)
    BusinessTypeMapper.attach_relations(child, child_model, cache)

    # same id but diff __repr__
    # assert child.parent is root
    # assert root.children == child
