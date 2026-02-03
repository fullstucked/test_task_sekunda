from __future__ import annotations

from domain.entities.base import Entity
from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.exceptions.org_err import OrganizationInvariantError
from domain.val_objs.ids import OrganizationId
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber


class Organization(Entity[OrganizationId]):
    """
    Aggregate root representing an organization.
    Contains business rules, invariants, and domain behavior.
    """

    def __init__(
        self,
        id_: OrganizationId,
        name: OrganizationName,
        phone_numbers: list[PhoneNumber],
        facility: Facility,
        business: list[BusinessType],
    ) -> None:
        super().__init__(id_=id_)
        self.name = name
        self.phone_numbers = list(phone_numbers)
        self.facility = facility
        self.business_types = list(business)

        self._validate_invariants()

    # ---------------------------------------------------------
    # Name
    # ---------------------------------------------------------

    def change_name(self, new_name: OrganizationName) -> None:
        self.name = new_name

    # ---------------------------------------------------------
    # Phone numbers
    # ---------------------------------------------------------

    def add_phone_number(self, phone: PhoneNumber) -> None:
        if phone in self.phone_numbers:
            raise OrganizationInvariantError("Phone number already exists")
        self.phone_numbers.append(phone)

    def remove_phone_number(self, phone: PhoneNumber) -> None:
        if phone not in self.phone_numbers:
            raise OrganizationInvariantError("Phone number not found")

        if len(self.phone_numbers) == 1:
            raise OrganizationInvariantError(
                "Organization must have at least one phone number"
            )

        self.phone_numbers.remove(phone)

    # ---------------------------------------------------------
    # Facility
    # ---------------------------------------------------------

    def assign_facility(self, facility: Facility) -> None:
        self.facility = facility

    def move_to_new_facility(self, facility: Facility) -> None:
        """Semantic alias for clarity."""
        self.assign_facility(facility)

    # ---------------------------------------------------------
    # Business Types
    # ---------------------------------------------------------

    def add_business_type(self, bt: BusinessType) -> None:
        if bt in self.business_types:
            raise OrganizationInvariantError("Business type already assigned")
        self.business_types.append(bt)

    def remove_business_type(self, bt: BusinessType) -> None:
        if bt not in self.business_types:
            raise OrganizationInvariantError("Business type not assigned")
        self.business_types.remove(bt)

    def has_business_type(self, bt: BusinessType) -> bool:
        return bt in self.business_types

    def business_type_names(self) -> list[str]:
        return [bt.name.value for bt in self.business_types]

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------

    def _validate_invariants(self) -> None:
        if not self.phone_numbers:
            raise OrganizationInvariantError(
                "Organization must have at least one phone number"
            )

        if not self.business_types:
            raise OrganizationInvariantError(
                "Organization must have at least one business type"
            )

        if self.facility is None:
            raise OrganizationInvariantError(
                "Organization must have a facility assigned"
            )
