import pytest
from domain.exceptions.base import DomainTypeError
from domain.exceptions.facility_err import InvalidAddressError
from domain.val_objs.address import Address


def test_address_valid():
    a = Address("Main Street 10")
    assert a.address == "Main Street 10"


def test_address_empty():
    with pytest.raises(InvalidAddressError):
        Address("")


def test_address_whitespace():
    with pytest.raises(InvalidAddressError):
        Address("   ")


def test_address_invalid_type():
    with pytest.raises(DomainTypeError):
        Address(123)


def test_address_repr():
    a = Address("Test")
    assert "Test" in repr(a)
