from domain.entities.organization import Organization
from domain.val_objs.ids import OrganizationId
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber
from infra.db.models.business_type import BusinessTypeModel
from infra.db.models.org import OrganizationModel
from infra.db.models.phone import PhoneModel
from infra.repositories.mappers.business_type_mapper import BusinessTypeMapper
from infra.repositories.mappers.facility_mapper import FacilityMapper


class OrganizationMapper:
    @staticmethod
    def to_domain(model: OrganizationModel) -> Organization:
        facility = FacilityMapper.to_domain(model.facility)

        business_types = [BusinessTypeMapper.to_domain(bt) for bt in model.activities]

        bt_cache = {bt.id_.value: bt for bt in business_types}
        for bt_model in model.activities:
            BusinessTypeMapper.attach_relations(
                bt_cache[bt_model.id], bt_model, bt_cache
            )

        return Organization(
            id_=OrganizationId(model.id),
            name=OrganizationName(model.name),
            phone_numbers=[PhoneNumber(p.phone_number) for p in model.phone_numbers],
            facility=facility,
            business_types=business_types,
        )

    @staticmethod
    def to_model(entity: Organization) -> OrganizationModel:
        model = OrganizationModel(
            id=entity.id_.value,
            name=entity.name.value,
            facility_id=entity.facility.id_.value,
        )

        model.phone_numbers = [
            PhoneModel(phone_number=p.value, org_id=entity.id_.value)
            for p in entity.phone_numbers
        ]

        model.activities = [
            BusinessTypeModel(
                id=bt.id_.value,
                name=bt.name.value,
                parent_id=bt.parent.id_.value if bt.parent else None,
            )
            for bt in entity.business_types
        ]

        return model
