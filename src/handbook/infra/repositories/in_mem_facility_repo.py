from __future__ import annotations

from math import radians, sin, cos, sqrt, atan2
from typing import Sequence
from uuid import UUID

from domain.entities.facility import Facility
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId
from domain.exceptions.base import DomainResourceNotFoundError

from domain.repositories.facility_repository import FacilityRepository


class InMemoryFacilityRepository(FacilityRepository):
    def __init__(self):
        # Use raw UUID keys for simplicity and type safety
        self._items: dict[UUID, Facility] = {}

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

    async def get_by_id(self, id: FacilityId) -> Facility:
        key = id.value
        try:
            return self._items[key]
        except KeyError:
            raise DomainResourceNotFoundError(f"Facility {id} not found")

    async def list_all(self) -> Sequence[Facility]:
        return list(self._items.values())

    async def save(self, facility: Facility) -> None:
        self._items[facility.id.value] = facility

    async def delete(self, facility: Facility) -> None:
        self._items.pop(facility.id.value, None)

    # ---------------------------------------------------------
    # Geographic queries
    # ---------------------------------------------------------

    async def list_in_radius(
        self,
        center: Coordinates,
        radius_meters: float,
    ) -> Sequence[Facility]:

        def haversine(c1: Coordinates, c2: Coordinates) -> float:
            R = 6371000  # meters

            lat1, lon1 = radians(float(c1.lat)), radians(float(c1.lon))
            lat2, lon2 = radians(float(c2.lat)), radians(float(c2.lon))

            dlat = lat2 - lat1
            dlon = lon2 - lon1

            a = (
                sin(dlat / 2) ** 2
                + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            )
            c = 2 * atan2(sqrt(a), sqrt(1 - a))

            return R * c

        return [
            f
            for f in self._items.values()
            if haversine(center, f.coordinates) <= radius_meters
        ]

    async def list_in_rectangle(
        self,
        p1: Coordinates,
        p2: Coordinates,
    ) -> Sequence[Facility]:

        min_lat = min(p1.lat, p2.lat)
        max_lat = max(p1.lat, p2.lat)
        min_lon = min(p1.lon, p2.lon)
        max_lon = max(p1.lon, p2.lon)

        return [
            f
            for f in self._items.values()
            if (
                min_lat <= f.coordinates.lat <= max_lat
                and min_lon <= f.coordinates.lon <= max_lon
            )
        ]
