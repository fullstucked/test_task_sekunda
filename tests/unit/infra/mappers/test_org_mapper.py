from domain.val_objs.address import Address
from domain.val_objs.business_name import BusinessName
from uuid import uuid4
from domain.val_objs.ids import OrganizationId
from decimal import Decimal
from domain.val_objs.coords import Coordinates
import uuid

from infra.db.models.org import OrganizationModel
from infra.db.models.facility import FacilityModel
from infra.db.models.phone import PhoneModel
from infra.db.models.business_type import BusinessTypeModel
from infra.repositories.mappers.organization_mapper import OrganizationMapper
from infra.repositories.mappers.facility_mapper import FacilityMapper
from infra.repositories.mappers.business_type_mapper import BusinessTypeMapper
from domain.entities.organization import Organization
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber
from domain.entities.facility import Facility
from domain.entities.business_type import BusinessType
from domain.val_objs.ids import FacilityId, BusinessTypeId


def test_org_to_domain_basic():
    fac_model = FacilityModel(
        id=uuid.uuid4(),
        address="HQ",
        lat="10",
        lon="20",
    )

    bt_model = BusinessTypeModel(
        id=uuid.uuid4(),
        name="Food",
        parent_id=None,
    )

    org_model = OrganizationModel(
        id=uuid.uuid4(),
        name="MyOrg",
        facility_id=fac_model.id,
    )

    org_model.facility = fac_model
    org_model.activities = [bt_model]
    org_model.phone_numbers = [PhoneModel(phone_number="123456", org_id=org_model.id)]

    org = OrganizationMapper.to_domain(org_model)

    assert org.name.value == "MyOrg"
    assert org.facility.address.address == "HQ"
    assert org.business_types[0].name.value == "Food"
    assert org.phone_numbers[0].value == "123456"


def test_org_to_model_basic():
    fac = Facility(
        id_=FacilityId(uuid.uuid4()),
        address=Address("HQwdq"),
        coordinates=Coordinates(Decimal(1), Decimal(1)),
    )

    bt = BusinessType(
        id_=BusinessTypeId(uuid.uuid4()),
        name=BusinessName("Food"),
        parent=None,
        children=[],
    )

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("MyOrg"),
        phone_numbers=[PhoneNumber("123456")],
        facility=fac,
        business_types=[bt],
    )

    model = OrganizationMapper.to_model(org)

    assert model.id == org.id_.value
    assert model.name == "MyOrg"
    assert model.facility_id == fac.id.value

    assert model.phone_numbers[0].phone_number == "123456"
    assert model.activities[0].id == bt.id.value
    assert model.activities[0].name == "Food"
