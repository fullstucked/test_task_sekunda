import pytest

from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from tests.integration.fixtures import make_facility


@pytest.mark.asyncio
async def test_facility_save_and_get(db_session):
    repo = FacilityRepositoryImpl(db_session)

    fac = make_facility("TestFacility")
    await repo.save(fac)
    await db_session.commit()

    loaded = await repo.get_by_id(fac.id)
    assert loaded.id == fac.id
    assert loaded.address.address == "TestFacility"


@pytest.mark.asyncio
async def test_facility_list_all(db_session):
    repo = FacilityRepositoryImpl(db_session)

    f1 = make_facility("AAAAA")
    f2 = make_facility("BBBBB")

    await repo.save(f1)
    await repo.save(f2)
    await db_session.commit()

    result = await repo.list_all()
    names = {f.address.address for f in result}

    assert names == {"AAAAA", "BBBBB"}


@pytest.mark.asyncio
async def test_facility_delete(db_session):
    repo = FacilityRepositoryImpl(db_session)

    fac = make_facility("DeleteMe")
    await repo.save(fac)
    await db_session.commit()

    await repo.delete(fac)
    await db_session.commit()

    with pytest.raises(Exception):
        await repo.get_by_id(fac.id)


@pytest.mark.asyncio
async def test_facility_list_in_radius(db_session):
    repo = FacilityRepositoryImpl(db_session)

    center = make_facility("Center", lat="10", lon="20")
    near = make_facility("Near", lat="10.0001", lon="20.0001")
    far = make_facility("Faraway", lat="50", lon="50")

    await repo.save(center)
    await repo.save(near)
    await repo.save(far)
    await db_session.commit()

    result = await repo.list_in_radius(center.coordinates, radius_meters=500)
    names = {f.address.address for f in result}

    assert "Near" in names
    assert "Faraway" not in names


@pytest.mark.asyncio
async def test_facility_list_in_rectangle(db_session):
    repo = FacilityRepositoryImpl(db_session)

    inside = make_facility("Inside", lat="10", lon="20")
    outside = make_facility("Outside", lat="50", lon="50")

    await repo.save(inside)
    await repo.save(outside)
    await db_session.commit()

    result = await repo.list_in_rectangle(
        inside.coordinates,
        make_facility(lat="11", lon="21").coordinates,
    )

    names = {f.address.address for f in result}
    assert names == {"Inside"}
