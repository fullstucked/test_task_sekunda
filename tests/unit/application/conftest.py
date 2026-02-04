from decimal import Decimal
from uuid import uuid4

from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.val_objs.address import Address
from domain.val_objs.business_name import BusinessName
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import BusinessTypeId, FacilityId, OrganizationId
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber


def make_facility(name: str, lat="10", lon="20"):
    return Facility(
        id_=FacilityId(uuid4()),
        address=Address(name),
        coordinates=Coordinates(lat=Decimal(lat), lon=Decimal(lon)),
    )


def make_bt(name: str, parent=None):
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName(name),
        parent=parent,
    )


def make_org(name: str, facility: Facility, *bts: BusinessType):
    return Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName(name),
        phone_numbers=[PhoneNumber("123456")],
        facility=facility,
        business_types=list(bts),
    )
