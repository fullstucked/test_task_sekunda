from __future__ import annotations

from typing import Sequence
from domain.entities.organization import Organization
from domain.entities.facility import Facility
from domain.entities.business_type import BusinessType
from domain.val_objs.ids import OrganizationId
from domain.exceptions.base import DomainResourceNotFoundError

from domain.repositories.organization_repository import OrganizationRepository
from domain.services.business_type_class_service import (
    BusinessTypeClassificationService,
)


class InMemoryOrganizationRepository(OrganizationRepository):
    def __init__(self):
        self._items: dict[OrganizationId, Organization] = {}

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    async def get_by_id(self, id: OrganizationId) -> Organization:
        try:
            return self._items[id]
        except KeyError:
            raise DomainResourceNotFoundError(f"Organization {id} not found")

    async def save(self, organization: Organization) -> None:
        self._items[organization.id] = organization

    async def delete(self, organization: Organization) -> None:
        self._items.pop(organization.id, None)

    # ---------------------------------------------------------
    # Domain-specific queries
    # ---------------------------------------------------------

    async def list_by_facility(self, facility: Facility) -> Sequence[Organization]:
        return [org for org in self._items.values() if org.facility == facility]

    async def list_by_business_type(self, bt: BusinessType) -> Sequence[Organization]:
        return [org for org in self._items.values() if bt in org.business_types]

    async def list_by_business_type_recursive(self, bt: BusinessType):
        descendants = BusinessTypeClassificationService.get_all_descendants(bt)
        all_types = {bt, *descendants}

        return [
            org
            for org in self._items.values()
            if any(t in all_types for t in org.business_types)
        ]

    async def list_by_any_business_type(
        self, types: Sequence[BusinessType]
    ) -> Sequence[Organization]:
        type_set = set(types)
        return [
            org
            for org in self._items.values()
            if any(t in type_set for t in org.business_types)
        ]

    async def search_by_name(self, query: str) -> Sequence[Organization]:
        q = query.lower()
        return [org for org in self._items.values() if q in org.name.value.lower()]
