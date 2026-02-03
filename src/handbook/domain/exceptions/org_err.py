from __future__ import annotations

from domain.exceptions.base import DomainError, DomainInvariantError, DomainTypeError


class OrganizationError(DomainError):
    """Base error for organization-related domain errors."""

    pass


class OrganizationInvariantError(OrganizationError, DomainInvariantError):
    """
    Raised when an organization's core business rules are violated.
    Combines organization-specific and invariant error characteristics.
    """

    pass


class OrganizationTypeError(DomainTypeError):
    """
    Raised when a value does not meet the type or format requirements
    for a BusinessType related instances
    """

    pass


class PhoneNumberError(DomainError):
    """Base error for phone number-related domain errors."""

    pass


class InvalidPhoneNumberError(PhoneNumberError):
    """
    Raised when a phone number does not meet validation criteria.
    Provides detailed context about the validation failure.
    """

    def __init__(self, phone_number: str, reason: str):
        super().__init__(
            f"Invalid phone number: {phone_number}",
            context={"phone_number": phone_number, "reason": reason},
        )
