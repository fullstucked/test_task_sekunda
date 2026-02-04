import pytest

from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl

from tests.integration.fixtures import make_org, make_facility, make_bt


@pytest.mark.asyncio
async def test_org_save_and_get(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt = make_bt("Food")

    await fac_repo.save(fac)
    await bt_repo.save(bt)
    await db_session.commit()

    org = make_org("MyOrg", fac, bt)
    await org_repo.save(org)
    await db_session.commit()

    loaded = await org_repo.get_by_id(org.id)

    assert loaded.name.value == "MyOrg"
    assert loaded.facility.address.address == "HQ"
    assert loaded.business_types[0].name.value == "Food"


@pytest.mark.asyncio
async def test_org_delete(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)

    fac = make_facility("HQ")
    await fac_repo.save(fac)
    await db_session.commit()

    org = make_org("DeleteMe", fac)
    await org_repo.save(org)
    await db_session.commit()

    await org_repo.delete(org)
    await db_session.commit()

    with pytest.raises(Exception):
        await org_repo.get_by_id(org.id)


@pytest.mark.asyncio
async def test_org_list_by_facility(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)

    fac1 = make_facility("A")
    fac2 = make_facility("B")

    await fac_repo.save(fac1)
    await fac_repo.save(fac2)
    await db_session.commit()

    o1 = make_org("O001", fac1)
    o2 = make_org("O002", fac1)
    o3 = make_org("O003", fac2)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await org_repo.save(o3)
    await db_session.commit()

    result = await org_repo.list_by_facility(fac1)
    names = {o.name.value for o in result}

    assert names == {"O001", "O002"}


@pytest.mark.asyncio
async def test_org_list_by_business_type(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt1 = make_bt("Food")
    bt2 = make_bt("Tech")

    await fac_repo.save(fac)
    await bt_repo.save(bt1)
    await bt_repo.save(bt2)
    await db_session.commit()

    o1 = make_org("O001", fac, bt1)
    o2 = make_org("O002", fac, bt2)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    result = await org_repo.list_by_business_type(bt1)
    names = {o.name.value for o in result}

    assert names == {"O001"}


@pytest.mark.asyncio
async def test_org_list_by_any_business_type(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt1 = make_bt("Food")
    bt2 = make_bt("Tech")

    await fac_repo.save(fac)
    await bt_repo.save(bt1)
    await bt_repo.save(bt2)
    await db_session.commit()

    o1 = make_org("O001", fac, bt1)
    o2 = make_org("O002", fac, bt2)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    result = await org_repo.list_by_any_business_type([bt1, bt2])
    names = {o.name.value for o in result}

    assert names == {"O001", "O002"}


@pytest.mark.asyncio
async def test_org_search_by_name(db_session):
    org_repo = OrganizationRepositoryImpl(db_session)
    fac_repo = FacilityRepositoryImpl(db_session)

    fac = make_facility("HQ")
    await fac_repo.save(fac)
    await db_session.commit()

    o1 = make_org("Coffee House", fac)
    o2 = make_org("Tech Hub", fac)

    await org_repo.save(o1)
    await org_repo.save(o2)
    await db_session.commit()

    result = await org_repo.search_by_name("coffee")
    names = {o.name.value for o in result}

    assert names == {"Coffee House"}
