from __future__ import annotations

from typing import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.exceptions.base import DomainResourceNotFoundError
from domain.repositories.organization_repository import OrganizationRepository
from domain.val_objs.ids import OrganizationId
from infra.db.models.business_type import BusinessTypeModel
from infra.db.models.links import organization_business_type
from infra.db.models.org import OrganizationModel
from infra.repositories.mappers.organization_mapper import OrganizationMapper


class OrganizationRepositoryImpl(OrganizationRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    async def get_by_id(self, id: OrganizationId) -> Organization:
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

        if model is None:
            raise DomainResourceNotFoundError(
                "Organization not found",
                context={"organization_id": str(id.value)},
            )

        return OrganizationMapper.to_domain(model)

    async def save(self, organization: Organization) -> None:
        model = OrganizationMapper.to_model(organization)
        await self._session.merge(model)

    async def delete(self, organization: Organization) -> None:
        db_model = await self._session.get(OrganizationModel, organization.id.value)
        if db_model is not None:
            await self._session.delete(db_model)

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    async def list_by_facility(self, facility: Facility) -> list[Organization]:
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.facility_id == facility.id.value)
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

    async def list_by_business_type(self, bt: BusinessType) -> list[Organization]:
        stmt = (
            select(OrganizationModel)
            .join(organization_business_type)
            .where(organization_business_type.c.business_type_id == bt.id.value)
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

    async def list_by_any_business_type(
        self,
        types: Iterable[BusinessType],
    ) -> list[Organization]:
        ids = [t.id.value for t in types]
        if not ids:
            return []

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
        return [OrganizationMapper.to_domain(m) for m in result.scalars().all()]

    async def search_by_name(self, query: str) -> list[Organization]:
        stmt = (
            select(OrganizationModel)
            .where(OrganizationModel.name.ilike(f"%{query}%"))
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
