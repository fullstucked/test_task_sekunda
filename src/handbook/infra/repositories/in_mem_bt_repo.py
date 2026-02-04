
from __future__ import annotations

from typing import Sequence
from uuid import UUID

from domain.entities.business_type import BusinessType
from domain.exceptions.base import DomainResourceNotFoundError
from domain.repositories.business_type_repository import BusinessTypeRepository
from domain.services.business_type_class_service import (
    BusinessTypeClassificationService,
)
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId


class InMemoryBusinessTypeRepository(BusinessTypeRepository):
    def __init__(self):
        # Store by raw UUID for type safety and simplicity
        self._items: dict[UUID, BusinessType] = {}

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    async def get_by_id(self, id: BusinessTypeId) -> BusinessType:
        key = id.value
        try:
            return self._items[key]
        except KeyError:
            raise DomainResourceNotFoundError(f"BusinessType {id} not found")

    async def get_by_name(self, name: BusinessName) -> BusinessType:
        for bt in self._items.values():
            if bt.name == name:
                return bt
        raise DomainResourceNotFoundError(f"BusinessType '{name.value}' not found")

    async def list_all(self) -> Sequence[BusinessType]:
        return list(self._items.values())

    async def save(self, bt: BusinessType) -> None:
        self._items[bt.id.value] = bt

    async def delete(self, bt: BusinessType) -> None:
        self._items.pop(bt.id.value, None)

    # ---------------------------------------------------------
    # Hierarchy-specific queries
    # ---------------------------------------------------------

    async def list_children(self, parent: BusinessType) -> Sequence[BusinessType]:
        return list(parent.children)

    async def list_roots(self) -> Sequence[BusinessType]:
        return [bt for bt in self._items.values() if bt.parent is None]

    async def list_descendants(self, root: BusinessType) -> Sequence[BusinessType]:
        return BusinessTypeClassificationService.get_all_descendants(root)
