from uuid import uuid4
from decimal import Decimal

from domain.entities.facility import Facility
from domain.entities.business_type import BusinessType
from domain.entities.organization import Organization

from domain.val_objs.ids import FacilityId, BusinessTypeId, OrganizationId
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.business_name import BusinessName
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber


def make_facility(name="AAAA", lat="10", lon="20"):
    return Facility(
        id_=FacilityId(uuid4()),
        address=Address(name),
        coordinates=Coordinates(lat=Decimal(lat), lon=Decimal(lon)),
    )


def make_bt(name="Food", parent=None):
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName(name),
        parent=parent,
    )


def make_org(name="Org", facility=None, *bts):
    if not bts:
        # provide a default business type
        bts = [make_bt()]
    unique_phone = PhoneNumber(str(uuid4().int)[:12])
    return Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName(name),
        phone_numbers=[unique_phone],
        facility=facility,
        business_types=list(bts),
    )
