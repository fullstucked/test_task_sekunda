from dataclasses import dataclass
from uuid import UUID

from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class OrganizationId(ValueObject):
    value: UUID


@dataclass(frozen=True, slots=True, repr=False)
class FacilityId(ValueObject):
    value: UUID


@dataclass(frozen=True, slots=True, repr=False)
class BusinessTypeId(ValueObject):
    value: UUID
