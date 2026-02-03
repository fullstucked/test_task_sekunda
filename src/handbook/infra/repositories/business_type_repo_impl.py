from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from domain.entities.business_type import BusinessType
from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId
from infra.db.models.business_type import BusinessTypeModel
from infra.repositories.mappers.business_type_mapper import BusinessTypeMapper


class BusinessTypeRepositoryImpl(BusinessTypeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    # ---------------------------------------------------------
    # Load a single BusinessType by ID
    # ---------------------------------------------------------
    async def get_by_id(self, id_: BusinessTypeId) -> BusinessType | None:
        stmt = (
            select(BusinessTypeModel)
            .where(BusinessTypeModel.id == id_.value)
            .options(
                selectinload(BusinessTypeModel.children),
                selectinload(BusinessTypeModel.parent),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return await self._map_tree(model) if model else None

    # ---------------------------------------------------------
    # Load a single BusinessType by name
    # ---------------------------------------------------------
    async def get_by_name(self, name: BusinessName) -> BusinessType | None:
        stmt = (
            select(BusinessTypeModel)
            .where(BusinessTypeModel.name == name.value)
            .options(
                selectinload(BusinessTypeModel.children),
                selectinload(BusinessTypeModel.parent),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return await self._map_tree(model) if model else None

    # ---------------------------------------------------------
    # Load all BusinessTypes
    # ---------------------------------------------------------
    async def list_all(self) -> list[BusinessType]:
        stmt = select(BusinessTypeModel).options(
            selectinload(BusinessTypeModel.children),
            selectinload(BusinessTypeModel.parent),
            raiseload("*"),
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        # First pass: create domain objects
        cache: dict[UUID, BusinessType] = {
            m.id: BusinessTypeMapper.to_domain(m) for m in models
        }

        # Second pass: attach relations
        for m in models:
            BusinessTypeMapper.attach_relations(cache[m.id], m, cache)

        return list(cache.values())

    # ---------------------------------------------------------
    # Save / delete
    # ---------------------------------------------------------
    async def save(self, bt: BusinessType) -> None:
        model = BusinessTypeMapper.to_model(bt)
        self._session.add(model)

    async def delete(self, bt: BusinessType) -> None:
        model = BusinessTypeMapper.to_model(bt)
        await self._session.delete(model)

    # ---------------------------------------------------------
    # Internal helper: build the full tree
    # ---------------------------------------------------------
    async def _map_tree(self, root_model: BusinessTypeModel) -> BusinessType:
        stmt = select(BusinessTypeModel).options(
            selectinload(BusinessTypeModel.children),
            selectinload(BusinessTypeModel.parent),
            raiseload("*"),
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        # First pass: create domain objects
        cache: dict[UUID, BusinessType] = {
            m.id: BusinessTypeMapper.to_domain(m) for m in models
        }

        # Second pass: attach relations
        for m in models:
            BusinessTypeMapper.attach_relations(cache[m.id], m, cache)

        return cache[root_model.id]
