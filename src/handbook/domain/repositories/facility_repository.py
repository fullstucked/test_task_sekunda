from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from domain.entities.facility import Facility
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId


class FacilityRepository(ABC):
    """
    Repository interface for Facility entity.
    Persistence-agnostic, domain-focused.
    """

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    @abstractmethod
    async def get_by_id(self, id: FacilityId) -> Facility:
        """
        Retrieve a facility by its unique identifier.
        Raises DomainResourceNotFoundError if not found.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_all(self) -> Sequence[Facility]:
        """
        Retrieve all facilities.
        """
        raise NotImplementedError

    @abstractmethod
    async def save(self, facility: Facility) -> None:
        """
        Persist a new or updated facility.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, facility: Facility) -> None:
        """
        Delete a facility.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Geographic queries
    # ---------------------------------------------------------

    @abstractmethod
    async def list_in_radius(
        self,
        center: Coordinates,
        radius_meters: float,
    ) -> Sequence[Facility]:
        """
        Retrieve facilities within a given radius from a center point.
        """
        raise NotImplementedError

    @abstractmethod
    async def list_in_rectangle(
        self,
        p1: Coordinates,
        p2: Coordinates,
    ) -> Sequence[Facility]:
        """
        Retrieve facilities inside a rectangular bounding box defined
        by two opposite corner coordinates (p1 and p2).
        """
        raise NotImplementedError
