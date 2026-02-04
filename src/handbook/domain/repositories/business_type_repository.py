from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from domain.entities.business_type import BusinessType
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId


class BusinessTypeRepository(ABC):
    """
    Repository interface for BusinessType entity.
    Persistence-agnostic, domain-focused.
    """

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    @abstractmethod
    async def get_by_id(self, id: BusinessTypeId) -> BusinessType:
        """
        Retrieve a business type by ID.
        Raises DomainResourceNotFoundError if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_name(self, name: BusinessName) -> BusinessType:
        """
        Retrieve a business type by its name.
        Raises DomainResourceNotFoundError if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> Sequence[BusinessType]:
        """Return all business types."""
        raise NotImplementedError

    @abstractmethod
    async def save(self, bt: BusinessType) -> None:
        """Persist a new or updated business type."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, bt: BusinessType) -> None:
        """Delete a business type."""
        raise NotImplementedError

    # ---------------------------------------------------------
    # Hierarchy-specific queries
    # ---------------------------------------------------------

    @abstractmethod
    async def list_children(self, parent: BusinessType) -> Sequence[BusinessType]:
        """Return direct children of a business type."""
        raise NotImplementedError

    @abstractmethod
    async def list_roots(self) -> Sequence[BusinessType]:
        """Return all business types with no parent."""
        raise NotImplementedError

    @abstractmethod
    async def list_descendants(self, root: BusinessType) -> Sequence[BusinessType]:
        """Return all descendants of a business type (recursive)."""
        raise NotImplementedError
