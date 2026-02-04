import pytest
from domain.exceptions.base import DomainTypeError
from domain.exceptions.org_err import InvalidPhoneNumberError
from domain.val_objs.phone import PhoneNumber


def test_phone_valid():
    phone = PhoneNumber("+123456789")
    assert phone.value == "+123456789"


def test_phone_too_short():
    with pytest.raises(DomainTypeError):
        PhoneNumber("123")


def test_phone_invalid_chars():
    with pytest.raises(InvalidPhoneNumberError):
        PhoneNumber("12A456")


def test_phone_invalid_start():
    with pytest.raises(InvalidPhoneNumberError):
        PhoneNumber("-123456")


def test_phone_repr():
    phone = PhoneNumber("+1234567")
    assert "+1234567" in repr(phone)
