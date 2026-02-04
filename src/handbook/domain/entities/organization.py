from __future__ import annotations

from domain.entities.base import Entity
from domain.entities.business_type import BusinessType
from domain.entities.facility import Facility
from domain.events.organization import OrganizationCreated, OrganizationNameChanged
from domain.exceptions.org_err import OrganizationInvariantError
from domain.val_objs.ids import OrganizationId
from domain.val_objs.organization_name import OrganizationName
from domain.val_objs.phone import PhoneNumber


class Organization(Entity[OrganizationId]):
    """
    Aggregate root representing an organization.
    """

    def __init__(
        self,
        id_: OrganizationId,
        name: OrganizationName,
        phone_numbers: list[PhoneNumber],
        facility: Facility,
        business_types: list[BusinessType],
    ) -> None:
        super().__init__(id_=id_)
        self.name = name
        self._phone_numbers = list(phone_numbers)
        self.facility = facility
        self._business_types = list(business_types)

        self._validate_invariants()
        self.record_event(OrganizationCreated(organization_id=id_))

    # ---------------------------------------------------------
    # Properties (read-only views)
    # ---------------------------------------------------------

    @property
    def phone_numbers(self) -> tuple[PhoneNumber, ...]:
        return tuple(self._phone_numbers)

    @property
    def business_types(self) -> tuple[BusinessType, ...]:
        return tuple(self._business_types)

    # ---------------------------------------------------------
    # Name
    # ---------------------------------------------------------

    def change_name(self, new_name: OrganizationName) -> None:
        old = self.name
        self.name = new_name
        self.record_event(
            OrganizationNameChanged(
                organization_id=self.id,
                old_name=old,
                new_name=new_name,
            )
        )

    # ---------------------------------------------------------
    # Phone numbers
    # ---------------------------------------------------------

    def add_phone_number(self, phone: PhoneNumber) -> None:
        if phone in self._phone_numbers:
            raise OrganizationInvariantError("Phone number already exists")
        self._phone_numbers.append(phone)

    def remove_phone_number(self, phone: PhoneNumber) -> None:
        if phone not in self._phone_numbers:
            raise OrganizationInvariantError("Phone number not found")

        if len(self._phone_numbers) == 1:
            raise OrganizationInvariantError(
                "Organization must have at least one phone number"
            )

        self._phone_numbers.remove(phone)

    # ---------------------------------------------------------
    # Facility
    # ---------------------------------------------------------

    def reassign_facility(self, facility: Facility) -> None:
        self.facility = facility

    # ---------------------------------------------------------
    # Business Types
    # ---------------------------------------------------------

    def add_business_type(self, bt: BusinessType) -> None:
        if bt in self._business_types:
            raise OrganizationInvariantError("Business type already assigned")
        self._business_types.append(bt)

    def remove_business_type(self, bt: BusinessType) -> None:
        if bt not in self._business_types:
            raise OrganizationInvariantError("Business type not assigned")

        if len(self._business_types) == 1:
            raise OrganizationInvariantError(
                "Organization must have at least one business type"
            )

        self._business_types.remove(bt)

    def has_business_type(self, bt: BusinessType) -> bool:
        return bt in self._business_types

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------

    def _validate_invariants(self) -> None:
        if not self._phone_numbers:
            raise OrganizationInvariantError(
                "Organization must have at least one phone number"
            )

        if not self._business_types:
            raise OrganizationInvariantError(
                "Organization must have at least one business type"
            )

        if self.facility is None:
            raise OrganizationInvariantError(
                "Organization must have a facility assigned"
            )
