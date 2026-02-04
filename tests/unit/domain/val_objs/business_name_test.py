import pytest
from domain.exceptions.business_type_err import BusinessTypeTypeError
from domain.val_objs.business_name import BusinessName


def test_business_name_valid():
    b = BusinessName("Food")
    assert b.value == "Food"


def test_business_name_too_short():
    with pytest.raises(BusinessTypeTypeError):
        BusinessName("Abc")


def test_business_name_too_long():
    with pytest.raises(BusinessTypeTypeError):
        BusinessName("A" * 200)


# def test_business_name_invalid_chars():
#     with pytest.raises(BusinessTypeTypeError):
#         BusinessName("Invalid@Name")
#
#
# def test_business_name_invalid_sequence():
#     with pytest.raises(BusinessTypeTypeError):
#         BusinessName("Bad..Name")
#

def test_business_name_repr():
    b = BusinessName("Test")
    assert "Test" in repr(b)
