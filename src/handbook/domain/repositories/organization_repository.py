from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.val_objs.ids import OrganizationId


class OrganizationRepository(ABC):
    """
    Repository interface for the Organization aggregate.
    Persistence-agnostic, domain-focused.
    """

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    @abstractmethod
    async def get_by_id(self, id: OrganizationId) -> Organization:
        """
        Retrieve an organization by ID.
        Raises DomainResourceNotFoundError if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, organization: Organization) -> None:
        """Persist a new or updated organization."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, organization: Organization) -> None:
        """Delete an organization."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Domain-specific queries
    # ---------------------------------------------------------

    @abstractmethod
    async def list_by_facility(self, facility: Facility) -> Sequence[Organization]:
        """Organizations located in a specific facility."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_business_type(self, bt: BusinessType) -> Sequence[Organization]:
        """Organizations with a specific business type (non-recursive)."""
        raise NotImplementedError

    @abstractmethod
    async def list_by_any_business_type(
        self, types: Sequence[BusinessType]
    ) -> Sequence[Organization]:
        """Organizations matching ANY of the given business types."""
        raise NotImplementedError

    @abstractmethod
    async def search_by_name(self, query: str) -> Sequence[Organization]:
        """Case-insensitive substring search."""
        raise NotImplementedError
