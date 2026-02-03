from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from domain.entities.facility import Facility
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId


class FacilityRepository(ABC):
    """
    Repository interface for Facility entity.
    Provides methods for persistence and geographic queries.
    """

    @abstractmethod
    async def get_by_id(self, id: FacilityId) -> Facility:
        """
        Retrieve a facility by its unique identifier.

        :param id_: Unique facility identifier
        :return: Facility instance or None if not found
        """
        pass

    @abstractmethod
    async def list_all(self) -> Iterable[Facility]:
        """
        Retrieve all facilities in the system.

        :return: Iterable of all facilities
        """
        pass

    @abstractmethod
    async def save(self, facility: Facility) -> None:
        """
        Persist a new or updated facility.

        :param facility: Facility to save
        """
        pass

    @abstractmethod
    async def delete(self, facility: Facility) -> None:
        """
        Remove an existing facility.

        :param facility: Facility to delete
        """
        pass

    # --- Geographic query methods ---

    @abstractmethod
    async def list_in_radius(
        self, center: Coordinates, radius_meters: float
    ) -> Iterable[Facility]:
        """
        Retrieve facilities within a specified radius from a center point.

        :param center: Central coordinates for the search
        :param radius_meters: Search radius in meters
        :return: Iterable of facilities within the radius
        """
        pass

    @abstractmethod
    async def list_in_rectangle(
        self,
        p1: Coordinates,
        p2: Coordinates,
    ) -> Iterable[Facility]:
        """
        Retrieve facilities within a rectangular bounding box.

        :param min_lat: Minimum latitude of the bounding box
        :param max_lat: Maximum latitude of the bounding box
        :param min_lon: Minimum longitude of the bounding box
        :param max_lon: Maximum longitude of the bounding box
        :return: Iterable of facilities within the bounding box
        """
        pass
