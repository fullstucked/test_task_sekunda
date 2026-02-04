from dataclasses import dataclass, field
from decimal import Decimal

from domain.exceptions.base import DomainTypeError
from domain.exceptions.facility_err import InvalidCoordinatesError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Coordinates(ValueObject):
    lat: Decimal = field(repr=True)
    lon: Decimal = field(repr=True)

    def __post_init__(self) -> None:
        if not isinstance(self.lat, Decimal) or not isinstance(self.lon, Decimal):
            raise DomainTypeError(message="Wrong type try Decimal")

        if not (-90 <= self.lat <= 90):
            raise InvalidCoordinatesError(
                latitude=self.lat,
                longitude=self.lon,
                reason="Latitude must be between -90 and 90",
            )

        if not (-180 <= self.lon <= 180):
            raise InvalidCoordinatesError(
                latitude=self.lat,
                longitude=self.lon,
                reason="Longitude must be between -180 and 180",
            )
