class DomainError(Exception):
    """
    Base class for all domain-specific errors.
    Provides a consistent error handling mechanism for domain logic violations.
    """

    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message)
        self.context = context or {}

    def __repr__(self) -> str:
        context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
        return f"{self.__class__.__name__}(message='{self.args[0]}', context={{{context_str}}})"


class DomainInvariantError(DomainError):
    """
    Raised when a domain entity's core business rules or invariants are violated.
    Indicates a fundamental constraint in the domain model has been broken.
    """

    pass


class DomainValidationError(DomainError):
    """
    Raised when input validation fails for domain objects.
    Provides detailed information about validation failures.
    """

    pass


class DomainTypeError(DomainError):
    """
    Raised when a value does not meet the type or format requirements
    for a specific domain value object.
    """

    pass


class DomainBusinessRuleError(DomainInvariantError):
    """
    Raised when a specific business rule or complex domain logic is violated.
    """

    pass


class DomainResourceNotFoundError(DomainError):
    pass
