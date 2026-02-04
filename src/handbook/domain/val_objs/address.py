from dataclasses import dataclass, field

from domain.exceptions.base import DomainTypeError
from domain.exceptions.facility_err import InvalidAddressError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Address(ValueObject):
    address: str = field(repr=True)

    def __post_init__(self) -> None:

        if not isinstance(self.address, str):
            raise DomainTypeError("Address must be a string")

        if not self.address.strip():
            raise InvalidAddressError(address=self.address, reason="Address cannot be empty")
