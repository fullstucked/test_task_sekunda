from domain.exceptions.base import DomainError, DomainInvariantError, DomainTypeError


class OrganizationError(DomainError):
    pass


class OrganizationInvariantError(OrganizationError, DomainInvariantError):
    pass


class OrganizationTypeError(DomainTypeError):
    pass


class PhoneNumberError(DomainError):
    pass


class InvalidPhoneNumberError(PhoneNumberError):
    def __init__(self, phone_number: str, reason: str):
        super().__init__(
            f"Invalid phone number: {phone_number}",
            context={"phone_number": phone_number, "reason": reason},
        )
