from __future__ import annotations

from domain.entities.base import Entity
from domain.exceptions.facility_err import FacilityInvariantError
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId


class Facility(Entity[FacilityId]):
    """
    Facility entity.
    Represents a physical location with an address and coordinates.
    """

    def __init__(
        self,
        id_: FacilityId,
        address: Address,
        coordinates: Coordinates,
    ) -> None:
        super().__init__(id_=id_)
        self._address = address
        self._coordinates = coordinates

        self._validate_invariants()

    # ---------------------------------------------------------
    # Properties (read-only)
    # ---------------------------------------------------------

    @property
    def address(self) -> Address:
        return self._address

    @property
    def coordinates(self) -> Coordinates:
        return self._coordinates

    # ---------------------------------------------------------
    # Address
    # ---------------------------------------------------------

    def update_address(self, new_address: Address) -> None:
        self._address = new_address
        self._validate_invariants()

    # ---------------------------------------------------------
    # Coordinates
    # ---------------------------------------------------------

    def update_coordinates(self, new_coords: Coordinates) -> None:
        self._coordinates = new_coords
        self._validate_invariants()

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------

    def _validate_invariants(self) -> None:
        if self._address is None:
            raise FacilityInvariantError("Facility must have an address")

        if self._coordinates is None:
            raise FacilityInvariantError("Facility must have coordinates")
