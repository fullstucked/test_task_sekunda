from dataclasses import dataclass, field
from uuid import UUID

from domain.exceptions.base import DomainTypeError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class OrganizationId(ValueObject):
    value: UUID = field(repr=True)

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise DomainTypeError("OrganizationId.value must be a UUID")


@dataclass(frozen=True, slots=True, repr=False)
class FacilityId(ValueObject):
    value: UUID = field(repr=True)

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise DomainTypeError("FacilityId.value must be a UUID")


@dataclass(frozen=True, slots=True, repr=False)
class BusinessTypeId(ValueObject):
    value: UUID = field(repr=True)

    def __post_init__(self) -> None:
        if not isinstance(self.value, UUID):
            raise DomainTypeError("BusinessTypeId.value must be a UUID")
