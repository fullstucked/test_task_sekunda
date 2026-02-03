from dataclasses import dataclass
from decimal import Decimal

from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Coordinates(ValueObject):
    lat: Decimal
    lon: Decimal

    def __post_init__(self):
        if not (-90 <= self.lat <= 90):
            raise ValueError("Latitude out of range")
        if not (-180 <= self.lon <= 180):
            raise ValueError("Longitude out of range")

    def distance_to(self, other: "Coordinates") -> float: ...
