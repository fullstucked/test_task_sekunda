from decimal import Decimal

import pytest
from domain.exceptions.base import DomainTypeError
from domain.exceptions.facility_err import InvalidCoordinatesError
from domain.val_objs.coords import Coordinates


def test_coordinates_valid():
    c = Coordinates(lat=Decimal("10"), lon=Decimal("20"))
    assert c.lat == Decimal("10")
    assert c.lon == Decimal("20")


def test_coordinates_invalid_lat():
    with pytest.raises(InvalidCoordinatesError):
        Coordinates(lat=Decimal("200"), lon=Decimal("0"))


def test_coordinates_invalid_lon():
    with pytest.raises(InvalidCoordinatesError):
        Coordinates(lat=Decimal("0"), lon=Decimal("500"))


def test_coordinates_invalid_type():
    with pytest.raises(DomainTypeError):
        Coordinates(lat=10, lon=20)  # ints not allowed


def test_coordinates_repr():
    c = Coordinates(lat=Decimal("1"), lon=Decimal("2"))
    assert "1" in repr(c)
    assert "2" in repr(c)
