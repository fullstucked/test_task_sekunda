import pytest
from uuid import uuid4
from decimal import Decimal

from domain.entities.facility import Facility
from domain.val_objs.ids import FacilityId
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.exceptions.facility_err import InvalidAddressError
from domain.exceptions.facility_err import InvalidCoordinatesError


def test_create_facility():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Main Street 10"),
        coordinates=Coordinates(lat=Decimal("55.75"), lon=Decimal("37.61")),
    )

    assert f.address.address == "Main Street 10"
    assert f.coordinates.lat == Decimal("55.75")
    assert f.coordinates.lon == Decimal("37.61")


def test_update_address():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Old Street 1"),
        coordinates=Coordinates(lat=Decimal("10"), lon=Decimal("20")),
    )

    new_addr = Address("New Street 2")
    f.update_address(new_addr)

    assert f.address == new_addr


def test_update_coordinates():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Main St"),
        coordinates=Coordinates(lat=Decimal("10"), lon=Decimal("20")),
    )

    new_coords = Coordinates(lat=Decimal("50"), lon=Decimal("30"))
    f.update_coordinates(new_coords)

    assert f.coordinates == new_coords


def test_update_address_invalid():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Main St"),
        coordinates=Coordinates(lat=Decimal("10"), lon=Decimal("20")),
    )

    with pytest.raises(InvalidAddressError):
        f.update_address(Address(""))


def test_update_coordinates_invalid():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Main St"),
        coordinates=Coordinates(lat=Decimal("10"), lon=Decimal("20")),
    )

    with pytest.raises(InvalidCoordinatesError):
        f.update_coordinates(Coordinates(lat=Decimal("200"), lon=Decimal("20")))


def test_facility_id_is_immutable():
    f = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Main St"),
        coordinates=Coordinates(lat=Decimal("10"), lon=Decimal("20")),
    )

    with pytest.raises(Exception):
        f.id = FacilityId(uuid4())
