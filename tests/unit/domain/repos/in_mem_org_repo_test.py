from decimal import Decimal
from uuid import uuid4

import pytest
from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.val_objs.address import Address
from domain.val_objs.business_name import BusinessName
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import BusinessTypeId, FacilityId, OrganizationId
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber
from infra.repositories.in_mem_org_repo import InMemoryOrganizationRepository


@pytest.fixture
def repo():
    return InMemoryOrganizationRepository()


def make_org(name: str, facility: Facility, bt: BusinessType):
    return Organization(
        id_=OrganizationId(uuid4()),
        name=OrganizationName(name),
        phone_numbers=[PhoneNumber("+1234567")],
        facility=facility,
        business_types=[bt],
    )


def make_facility(addr: str):
    return Facility(
        id_=FacilityId(uuid4()),
        address=Address(addr),
        coordinates=Coordinates(lat=Decimal("1"), lon=Decimal("1")),
    )


def make_bt(name: str, parent=None):
    return BusinessType(
        id_=BusinessTypeId(uuid4()),
        name=BusinessName(name),
        parent=parent,
    )


@pytest.mark.asyncio
async def test_save_and_get(repo):
    fac = make_facility("A")
    bt = make_bt("Food")
    org = make_org("TestOrg", fac, bt)

    await repo.save(org)
    loaded = await repo.get_by_id(org.id)

    assert loaded is org


@pytest.mark.asyncio
async def test_delete(repo):
    fac = make_facility("A")
    bt = make_bt("Food")
    org = make_org("TestOrg", fac, bt)

    await repo.save(org)
    await repo.delete(org)

    with pytest.raises(Exception):
        await repo.get_by_id(org.id)


@pytest.mark.asyncio
async def test_list_by_facility(repo):
    fac1 = make_facility("A")
    fac2 = make_facility("B")
    bt = make_bt("Food")

    org1 = make_org("OneOrg", fac1, bt)
    org2 = make_org("TwoOrg", fac2, bt)

    await repo.save(org1)
    await repo.save(org2)

    result = await repo.list_by_facility(fac1)
    assert result == [org1]


@pytest.mark.asyncio
async def test_list_by_business_type(repo):
    fac = make_facility("A")
    bt1 = make_bt("Food")
    bt2 = make_bt("Tech")

    org1 = make_org("OneOrg", fac, bt1)
    org2 = make_org("TwoOrg", fac, bt2)

    await repo.save(org1)
    await repo.save(org2)

    result = await repo.list_by_business_type(bt1)
    assert result == [org1]


@pytest.mark.asyncio
async def test_list_by_business_type_recursive(repo):
    fac = make_facility("A")
    root = make_bt("Food")
    child = make_bt("Meat", parent=root)

    org1 = make_org("OneOrg", fac, root)
    org2 = make_org("TwoOrg", fac, child)

    await repo.save(org1)
    await repo.save(org2)

    result = await repo.list_by_business_type_recursive(root)
    assert set(result) == {org1, org2}


@pytest.mark.asyncio
async def test_search_by_name(repo):
    fac = make_facility("A")
    bt = make_bt("Food")

    org1 = make_org("AlphaOrg", fac, bt)
    org2 = make_org("BetaOrg", fac, bt)

    await repo.save(org1)
    await repo.save(org2)

    result = await repo.search_by_name("alp")
    assert result == [org1]

@pytest.mark.asyncio
async def test_list_by_any_business_type(repo):
    fac = make_facility("AAAA")

    bt_food = make_bt("Food")
    bt_meat = make_bt("Meat", parent=bt_food)
    bt_tech = make_bt("Tech")

    org1 = make_org("FoodOrg", fac, bt_food)
    org2 = make_org("MeatOrg", fac, bt_meat)
    org3 = make_org("TechOrg", fac, bt_tech)

    await repo.save(org1)
    await repo.save(org2)
    await repo.save(org3)

    # Query for Food + Tech
    result = await repo.list_by_any_business_type([bt_food, bt_tech])

    assert set(result) == {org1, org3}
