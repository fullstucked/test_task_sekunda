from decimal import Decimal
from uuid import uuid4

import pytest
from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import (
    BusinessTypeId,
    FacilityId,
    OrganizationId,
)
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber

# -----------------------------
# Value Object Factories
# -----------------------------


@pytest.fixture
def org_name():
    return OrganizationName("TestOrg")


@pytest.fixture
def phone_number():
    return PhoneNumber("+123456789")


@pytest.fixture
def coords():
    return Coordinates(lat=Decimal("55.75"), lon=Decimal("37.61"))


@pytest.fixture
def address():
    return Address("Some Street 10")


# -----------------------------
# Entity Factories
# -----------------------------


@pytest.fixture
def facility(coords, address):
    return Facility(
        id_=FacilityId(uuid4()),
        address=address,
        coordinates=coords,
    )


@pytest.fixture
def business_type_root():
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name="RootType",
        parent=None,
    )


@pytest.fixture
def business_type_child(business_type_root):
    child = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name="ChildType",
        parent=business_type_root,
    )
    business_type_root.add_child(child)
    return child


@pytest.fixture
def organization(org_name, phone_number, facility, business_type_root):
    return Organization(
        id_=OrganizationId(uuid4()),
        name=org_name,
        phone_numbers=[phone_number],
        facility=facility,
        business_types=[business_type_root],
    )
