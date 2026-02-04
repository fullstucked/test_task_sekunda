from decimal import Decimal
from domain.exceptions.base import DomainError, DomainInvariantError


class FacilityError(DomainError):
    """Base error for facility-related domain errors."""

    pass


class FacilityInvariantError(FacilityError, DomainInvariantError):
    """
    Raised when a facility's core business rules are violated.
    Ensures facility-specific constraints are maintained.
    """

    pass


class AddressError(DomainError):
    """Base error for address-related domain errors."""

    pass


class InvalidAddressError(AddressError):
    """
    Raised when an address does not meet validation criteria.
    Provides detailed context about the address validation failure.
    """

    def __init__(self, address: str, reason: str):
        super().__init__(
            f"Invalid address: {address}",
            context={"address": address, "reason": reason},
        )


class CoordinatesError(DomainError):
    """Base error for geographical coordinates-related domain errors."""

    pass


class InvalidCoordinatesError(CoordinatesError):
    """
    Raised when coordinates do not meet validation criteria.
    Provides detailed context about coordinate validation failure.
    """

    def __init__(self, latitude: Decimal, longitude: Decimal, reason: str):
        super().__init__(
            f"Invalid coordinates: {latitude}, {longitude}",
            context={"latitude": latitude, "longitude": longitude, "reason": reason},
        )
