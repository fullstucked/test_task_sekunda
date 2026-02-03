from domain.exceptions.base import DomainError, DomainInvariantError, DomainTypeError


class BusinessTypeError(DomainError):
    """Base error for business type-related domain errors."""

    pass


class BusinessTypeHierarchyError(BusinessTypeError, DomainInvariantError):
    """
    Raised when business type hierarchy rules are violated.
    Handles issues like cycle detection, depth limitations, etc.
    """

    pass


class BusinessTypeTypeError(DomainTypeError):
    """
    Raised when a value does not meet the type or format requirements
    for a BusinessType related instances
    """

    pass
