from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, raiseload

from domain.entities.business_type import BusinessType
from domain.exceptions.base import DomainResourceNotFoundError
from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId

from infra.db.models.business_type import BusinessTypeModel
from infra.repositories.mappers.business_type_mapper import BusinessTypeMapper


class BusinessTypeRepositoryImpl(BusinessTypeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    async def _load_all_models(self) -> list[BusinessTypeModel]:
        stmt = (
            select(BusinessTypeModel)
            .options(
                selectinload(BusinessTypeModel.children),
                selectinload(BusinessTypeModel.parent),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()

    def _hydrate_tree(
        self, models: list[BusinessTypeModel]
    ) -> dict[UUID, BusinessType]:
        cache = {m.id: BusinessTypeMapper.to_domain(m) for m in models}
        for m in models:
            BusinessTypeMapper.attach_relations(cache[m.id], m, cache)
        return cache

    # ---------------------------------------------------------
    # Queries
    # ---------------------------------------------------------

    async def get_by_id(self, id: BusinessTypeId) -> BusinessType:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)

        if id.value not in cache:
            raise DomainResourceNotFoundError(
                "BusinessType not found",
                context={"business_type_id": str(id.value)},
            )

        return cache[id.value]

    async def get_by_name(self, name: BusinessName) -> BusinessType:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)

        for bt in cache.values():
            if bt.name.value == name.value:
                return bt

        raise DomainResourceNotFoundError(
            "BusinessType not found",
            context={"business_type_name": name.value},
        )

    async def list_all(self) -> list[BusinessType]:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)
        return list(cache.values())

    async def list_children(self, parent: BusinessType) -> list[BusinessType]:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)

        return [
            bt for bt in cache.values()
            if bt.parent and bt.parent.id.value == parent.id.value
        ]

    async def list_roots(self) -> list[BusinessType]:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)

        return [bt for bt in cache.values() if bt.parent is None]

    async def list_descendants(self, root: BusinessType) -> list[BusinessType]:
        models = await self._load_all_models()
        cache = self._hydrate_tree(models)

        result = []
        stack = [root.id.value]

        while stack:
            current = stack.pop()
            for bt in cache.values():
                if bt.parent and bt.parent.id.value == current:
                    result.append(bt)
                    stack.append(bt.id.value)

        return result

    # ---------------------------------------------------------
    # Persistence
    # ---------------------------------------------------------

    async def save(self, bt: BusinessType) -> None:
        model = BusinessTypeMapper.to_model(bt)
        await self._session.merge(model)

    async def delete(self, bt: BusinessType) -> None:
        db_model = await self._session.get(BusinessTypeModel, bt.id.value)
        if db_model is not None:
            await self._session.delete(db_model)
