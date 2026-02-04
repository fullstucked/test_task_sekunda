from uuid import uuid4

import pytest
from domain.exceptions.base import DomainTypeError
from domain.val_objs.ids import OrganizationId


def test_org_id_valid():
    oid = OrganizationId(uuid4())
    assert isinstance(oid.value, type(uuid4()))


def test_org_id_invalid():
    with pytest.raises(DomainTypeError):
        OrganizationId("not-a-uuid")


def test_id_repr():
    oid = OrganizationId(uuid4())
    assert str(oid.value) in repr(oid)
