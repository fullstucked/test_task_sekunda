from typing import Iterable

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import OrganizationId
from infra.db.models.business_type import BusinessTypeModel
from infra.db.models.links import organization_business_type
from infra.db.models.org import OrganizationModel
from infra.repositories.mappers.organization_mapper import OrganizationMapper


class OrganizationRepositoryImpl(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: OrganizationId):
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.id == id.value)
            .options(
                selectinload(OrganizationModel.facility),
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.children
                ),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.parent
                ),
                raiseload("*"),
            )
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return OrganizationMapper.to_domain(model) if model else None

    async def save(self, organization: Organization):
        model = OrganizationMapper.to_model(organization)
        self._session.add(model)

    async def delete(self, organization: Organization) -> None:
        model = OrganizationMapper.to_model(organization)
        await self._session.delete(model)

    async def list_by_facility(self, facility: Facility):
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.facility_id == facility.id_.value)
            .options(
                selectinload(OrganizationModel.facility),
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.children
                ),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.parent
                ),
            )
        )
        result = await self._session.execute(stmt)
        return [OrganizationMapper.to_domain(m) for m in result.scalars().all()]

    async def list_by_business_type(self, bt: BusinessType):
        stmt = (
            select(OrganizationModel)
            .join(organization_business_type)
            .where(organization_business_type.c.business_type_id == bt.id_.value)
            .options(
                selectinload(OrganizationModel.facility),
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.activities),
            )
        )
        result = await self._session.execute(stmt)
        return [OrganizationMapper.to_domain(m) for m in result.scalars().all()]

    async def list_by_business_types(self, types: Iterable[BusinessType]):
        ids = [t.id_.value for t in types]
        stmt = (
            select(OrganizationModel)
            .join(organization_business_type)
            .where(organization_business_type.c.business_type_id.in_(ids))
            .options(
                selectinload(OrganizationModel.facility),
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.children
                ),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.parent
                ),
            )
        )
        result = await self._session.execute(stmt)
        result = [OrganizationMapper.to_domain(m) for m in result.scalars().all()]
        return result

    async def search_by_name(self, query: str):
        stmt = (
            select(OrganizationModel)
            .where(func.lower(OrganizationModel.name).contains(query.lower()))
            .options(
                selectinload(OrganizationModel.facility),
                selectinload(OrganizationModel.phone_numbers),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.children
                ),
                selectinload(OrganizationModel.activities).selectinload(
                    BusinessTypeModel.parent
                ),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        return [OrganizationMapper.to_domain(m) for m in result.scalars().all()]
