from domain.entities.business_type import BusinessType
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId
from infra.db.models.business_type import BusinessTypeModel


class BusinessTypeMapper:
    @staticmethod
    def to_domain(model: BusinessTypeModel) -> BusinessType:
        return BusinessType(
            id_=BusinessTypeId(model.id),
            name=BusinessName(model.name),
            parent=None,
            children=[],
        )

    @staticmethod
    def attach_relations(
        domain_bt: BusinessType, model: BusinessTypeModel, cache: dict
    ):
        # parent
        if model.parent_id:
            parent = cache.get(model.parent_id)
            domain_bt.set_parent(parent)

        # children
        for child_model in model.children:
            child = cache[child_model.id]
            domain_bt.add_child(child)

    @staticmethod
    def to_model(entity: BusinessType) -> BusinessTypeModel:
        return BusinessTypeModel(
            id=entity.id_.value,
            name=entity.name.value,
            parent_id=entity.parent.id_.value if entity.parent else None,
        )
