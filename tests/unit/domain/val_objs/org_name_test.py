import pytest
from domain.exceptions.org_err import OrganizationTypeError
from domain.val_objs.organization_name import OrganizationName


def test_org_name_valid():
    name = OrganizationName("ValidName")
    assert name.value == "ValidName"


def test_org_name_too_short():
    with pytest.raises(OrganizationTypeError):
        OrganizationName("Abc")


def test_org_name_too_long():
    with pytest.raises(OrganizationTypeError):
        OrganizationName("A" * 50)

#
# def test_org_name_invalid_start():
#     with pytest.raises(OrganizationTypeError):
#         OrganizationName(".Invalid")
#
#
# def test_org_name_invalid_end():
#     with pytest.raises(OrganizationTypeError):
#         OrganizationName("Invalid.")
#
#
# def test_org_name_invalid_sequence():
#     with pytest.raises(OrganizationTypeError):
#         OrganizationName("Bad..Name")


def test_org_name_repr():
    name = OrganizationName("TestName")
    assert "TestName" in repr(name)
