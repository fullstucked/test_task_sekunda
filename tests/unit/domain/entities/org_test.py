from domain.exceptions.org_err import OrganizationInvariantError
from decimal import Decimal
import pytest
from uuid import uuid4

from domain.entities.organization import Organization
from domain.entities.facility import Facility
from domain.entities.business_type import BusinessType

from domain.val_objs.ids import (
    OrganizationId,
    FacilityId,
    BusinessTypeId,
)
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.business_name import BusinessName



def test_create_organization():
    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestOrg"),
        phone_numbers=[PhoneNumber("+1234567")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )

    assert org.name.value == "TestOrg"
    assert len(org.phone_numbers) == 1
    assert len(org.business_types) == 1


def test_change_name():
    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("OldName"),
        phone_numbers=[PhoneNumber("+1234567")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )

    org.change_name(OrganizationName("NewName"))
    assert org.name.value == "NewName"


def test_add_phone_number():
    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )

    new_phone = PhoneNumber("+2222222")
    org.add_phone_number(new_phone)

    assert new_phone in org.phone_numbers


def test_add_duplicate_phone_number():
    phone = PhoneNumber("+1111111")

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[phone],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )



    with pytest.raises(OrganizationInvariantError):
        org.add_phone_number(phone)


def test_remove_phone_number():
    phone = PhoneNumber("+1111111")
    phone2 = PhoneNumber("+1111112")

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[phone, phone2],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )


    org.remove_phone_number(phone)
    assert phone not in org.phone_numbers


def test_remove_nonexistent_phone_number():
    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )

    with pytest.raises(OrganizationInvariantError):
        org.remove_phone_number(PhoneNumber("+2222222"))


def test_change_facility():
    old_facility = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Old St 1"),
        coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
    )

    new_facility = Facility(
        id_=FacilityId(uuid4()),
        address=Address("New St 2"),
        coordinates=Coordinates(lat=Decimal(2), lon=Decimal(2)),
    )

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=old_facility,
        business_types=[
            BusinessType(
                id_=BusinessTypeId(uuid4()),
                name=BusinessName("Food"),
                parent=None,
            )
        ],
    )

    org.reassign_facility(new_facility)
    assert org.facility == new_facility


def test_add_business_type():
    bt = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )
    bt2 = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[bt2],
    )

    org.add_business_type(bt)
    assert bt in org.business_types


def test_add_duplicate_business_type():
    bt = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[bt],
    )

    with pytest.raises(OrganizationInvariantError):
        org.add_business_type(bt)


def test_remove_business_type():
    bt = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )

    bt2 = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )
    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[bt,bt2],
    )

    org.remove_business_type(bt)
    assert bt not in org.business_types


def test_remove_nonexistent_business_type():
    bt1 = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Food"),
        parent=None,
    )
    bt2 = BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName("Meat"),
        parent=None,
    )

    org = Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName("TestName"),
        phone_numbers=[PhoneNumber("+1111111")],
        facility=Facility(
            id_=FacilityId(uuid4()),
            address=Address("Main St 1"),
            coordinates=Coordinates(lat=Decimal(1), lon=Decimal(1)),
        ),
        business_types=[bt1],
    )

    with pytest.raises(OrganizationInvariantError):
        org.remove_business_type(bt2)
