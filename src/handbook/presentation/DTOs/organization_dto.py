from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.organization import Organization
from presentation.DTOs.business_types_dto import BusinessTypeDTO
from presentation.DTOs.facility_dto import FacilityDTO


class PhoneDTO(BaseModel):
    number: str = Field(
        ...,
        description="Phone number in international or local format.",
        example="+7 495 123-45-67",
        #pattern=r"^[\w\s\-\.,]{1,100}$",
    )


class OrganizationDTO(BaseModel):
    """
    DTO representing an organization with its facility, phone numbers,
    and associated business types.
    """

    id: UUID = Field(
        ...,
        description="Unique identifier of the organization.",
        example="99999999-9999-9999-9999-999999999999",
    )
    name: str = Field(
        ...,
        description="Human-readable name of the organization.",
        example="Coffee House №1",
    )
    phones: list[PhoneDTO] = Field(
        ...,
        description="List of phone numbers associated with the organization.",
        example=[{"number": "+7 495 123-45-67"}],
    )
    facility: FacilityDTO = Field(
        ...,
        description="Facility where the organization is located.",
        example={
            "id": "11111111-1111-1111-1111-111111111111",
            "address": "г. Москва, пр-т Мира 10",
            "lat": "55.790001",
            "lon": "37.630001",
        },
    )
    business_types: list[BusinessTypeDTO] = Field(
        ...,
        description="List of business types describing the organization's activity.",
        example=[
            {
                "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "name": "Restaurant",
                "parent_id": None,
            }
        ],
    )

    @staticmethod
    def from_domain(org: Organization):
        """
        Convert a domain Organization entity into a DTO.
        """
        return OrganizationDTO(
            id=org.id_.value,
            name=org.name.value,
            phones=[PhoneDTO(number=p.value) for p in org.phone_numbers],
            facility=FacilityDTO(
                id=org.facility.id_.value,
                address=org.facility.address.address,
                lat=str(org.facility.coordinates.lat),
                lon=str(org.facility.coordinates.lon),
            ),
            business_types=[
                BusinessTypeDTO(
                    id=bt.id_.value,
                    name=bt.name.value,
                    parent_id=bt.parent.id_.value if bt.parent else None,
                )
                for bt in org.business_types
            ],
        )
