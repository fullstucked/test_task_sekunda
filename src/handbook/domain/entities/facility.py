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
        self.address = address
        self.coordinates = coordinates

        self._validate_invariants()

    # ---------------------------------------------------------
    # Address
    # ---------------------------------------------------------

    def update_address(self, new_address: Address) -> None:
        """Replace the facility's address."""
        self.address = new_address
        self._validate_invariants()

    # ---------------------------------------------------------
    # Coordinates
    # ---------------------------------------------------------

    def update_coordinates(self, new_coords: Coordinates) -> None:
        """Replace the facility's coordinates."""
        self.coordinates = new_coords
        self._validate_invariants()

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------

    def _validate_invariants(self) -> None:
        if self.address is None:
            raise FacilityInvariantError("Facility must have an address")

        if self.coordinates is None:
            raise FacilityInvariantError("Facility must have coordinates")
