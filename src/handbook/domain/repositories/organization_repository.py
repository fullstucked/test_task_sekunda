from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.entities.organization import Organization
from domain.val_objs.ids import OrganizationId


class OrganizationRepository(ABC):
    """
    Repository interface for Organization aggregate.
    Defines all queries required by the domain and application use cases.
    Follows DDD principles of separation of concerns and persistence ignorance.
    """

    @abstractmethod
    async def get_by_id(self, id: OrganizationId) -> Optional[Organization]:
        """
        Retrieve an organization by its unique identifier.

        :param id_: Unique organization identifier
        :return: Organization instance or None if not found
        """
        pass

    @abstractmethod
    async def save(self, organization: Organization) -> None:
        """
        Persist a new or updated organization.

        :param organization: Organization to save
        """
        pass

    @abstractmethod
    async def delete(self, organization: Organization) -> None:
        """
        Remove an existing organization.

        :param organization: Organization to delete
        """
        pass

    # --- Domain-specific query methods as per requirements ---

    @abstractmethod
    async def list_by_facility(self, facility: Facility) -> Iterable[Organization]:
        """
        Retrieve all organizations located in a specific facility.

        :param facility: Facility to search organizations in
        :return: Iterable of organizations in the facility
        """
        pass

    @abstractmethod
    async def list_by_business_type(self, bt: BusinessType) -> Iterable[Organization]:
        """
        Retrieve organizations with a specific business type.
        Supports first-level business type matching.

        :param bt: Business type to search for
        :return: Iterable of organizations with the business type
        """
        pass

    @abstractmethod
    async def list_by_business_types(
        self, types: Iterable[BusinessType]
    ) -> Iterable[Organization]:
        """
        Retrieve organizations matching ANY of the given business types.
        Supports recursive search through business type hierarchy.

        :param types: Business types to search for
        :return: Iterable of organizations matching the types
        """
        pass

    @abstractmethod
    async def search_by_name(self, query: str) -> Iterable[Organization]:
        """
        Perform case-insensitive substring search on organization names.

        :param query: Search query string
        :return: Iterable of organizations matching the name
        """
        pass
