from fastapi import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from infra.db.session import get_session
from infra.repositories.business_type_repo_impl import BusinessTypeRepositoryImpl
from infra.repositories.facility_repo_impl import FacilityRepositoryImpl
from infra.repositories.organization_repo_impl import OrganizationRepositoryImpl


async def get_org_repo(session: AsyncSession = Depends(get_session)):
    return OrganizationRepositoryImpl(session)


async def get_facility_repo(session: AsyncSession = Depends(get_session)):
    return FacilityRepositoryImpl(session)


async def get_bt_repo(
    session: AsyncSession = Depends(get_session),
) -> BusinessTypeRepositoryImpl:
    try:
        repo = BusinessTypeRepositoryImpl(session)
        return repo
    except Exception as e:
        # Properly re-raise the exception
        raise HTTPException(status_code=500, detail=str(e)) from e
