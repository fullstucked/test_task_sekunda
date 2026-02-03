from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Optional

from domain.entities.business_type import BusinessType
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId


class BusinessTypeRepository(ABC):
    """
    Repository interface for BusinessType entity.
    Provides methods for managing business type hierarchies.
    """

    @abstractmethod
    async def get_by_id(self, id_: BusinessTypeId) -> Optional[BusinessType]:
        """
        Retrieve a business type by its unique identifier.

        :param id_: Unique business type identifier
        :return: BusinessType instance or None if not found
        """
        pass

    @abstractmethod
    async def get_by_name(self, name: BusinessName) -> Optional[BusinessType]:
        """
        Retrieve a business type by its name.

        :param name: Business type name
        :return: BusinessType instance or None if not found
        """
        pass

    @abstractmethod
    async def list_all(self) -> Iterable[BusinessType]:
        """
        Retrieve all business types in the system.

        :return: Iterable of all business types
        """
        pass

    @abstractmethod
    async def save(self, bt: BusinessType) -> None:
        """
        Persist a new or updated business type.

        :param bt: Business type to save
        """
        pass

    @abstractmethod
    async def delete(self, bt: BusinessType) -> None:
        """
        Remove an existing business type.

        :param bt: Business type to delete
        """
        pass
