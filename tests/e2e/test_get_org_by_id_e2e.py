import uuid

import httpx
import pytest
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl
from setup.app_factory import create_app

from tests.integration.fixtures import make_bt, make_facility, make_org


@pytest.mark.asyncio
async def test_get_org_by_id_e2e(db_session):
    """
    Full end‑to‑end test:
    FastAPI → DI → use‑case → repo_impl → mappers → DB → back to API response.
    """

    fac_repo = FacilityRepositoryImpl(db_session)
    bt_repo = BusinessTypeRepositoryImpl(db_session)
    org_repo = OrganizationRepositoryImpl(db_session)

    fac = make_facility("HQ")
    bt = make_bt("Food")

    await fac_repo.save(fac)
    await bt_repo.save(bt)
    await db_session.commit()

    org = make_org("MyOrg", fac, bt)
    await org_repo.save(org)
    await db_session.commit()

    app = create_app()

    async def override_get_db():
        yield db_session

    app.dependency_overrides = {"infra.db.dependency.get_db": override_get_db}

    # --- call API ---
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/v1/organizations/{org.id}")

    # --- assertions ---
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(org.id)
    assert data["name"] == "MyOrg"
    assert data["facility"]["address"] == "HQ"
    assert data["business_types"][0]["name"] == "Food"
    assert isinstance(uuid.UUID(data["id"]), uuid.UUID)
