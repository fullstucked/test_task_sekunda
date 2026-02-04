
from decimal import Decimal
from uuid import uuid4

import pytest
from domain.entities.facility import Facility
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId
from infra.repositories.in_mem_facility_repo import InMemoryFacilityRepository


@pytest.fixture
def repo():
    return InMemoryFacilityRepository()


def make_facility(lat: str, lon: str, addr: str = "X"):
    return Facility(
        id_=FacilityId(uuid4()),
        address=Address(addr),
        coordinates=Coordinates(lat=Decimal(lat), lon=Decimal(lon)),
    )


@pytest.mark.asyncio
async def test_save_and_get(repo):
    f = make_facility("10", "20")
    await repo.save(f)

    loaded = await repo.get_by_id(f.id)
    assert loaded is f


@pytest.mark.asyncio
async def test_delete(repo):
    f = make_facility("10", "20")
    await repo.save(f)
    await repo.delete(f)

    with pytest.raises(Exception):
        await repo.get_by_id(f.id)


@pytest.mark.asyncio
async def test_list_all(repo):
    f1 = make_facility("10", "20")
    f2 = make_facility("30", "40")

    await repo.save(f1)
    await repo.save(f2)

    result = await repo.list_all()
    assert set(result) == {f1, f2}


@pytest.mark.asyncio
async def test_list_in_radius(repo):
    center = Coordinates(lat=Decimal("0"), lon=Decimal("0"))

    near = make_facility("0.001", "0.001")  # ~157m away
    far = make_facility("1", "1")           # very far

    await repo.save(near)
    await repo.save(far)

    result = await repo.list_in_radius(center, radius_meters=500)
    assert result == [near]


@pytest.mark.asyncio
async def test_list_in_rectangle(repo):
    f1 = make_facility("10", "10")
    f2 = make_facility("20", "20")
    f3 = make_facility("30", "30")

    await repo.save(f1)
    await repo.save(f2)
    await repo.save(f3)

    p1 = Coordinates(lat=Decimal("5"), lon=Decimal("5"))
    p2 = Coordinates(lat=Decimal("25"), lon=Decimal("25"))

    result = await repo.list_in_rectangle(p1, p2)
    assert set(result) == {f1, f2}
