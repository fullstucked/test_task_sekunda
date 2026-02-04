from uuid import UUID
from pydantic import BaseModel, Field

from domain.entities.organization import Organization
from presentation.DTOs.business_types_dto import BusinessTypeDTO
from presentation.DTOs.facility_dto import FacilityDTO


class PhoneDTO(BaseModel):
    number: str = Field(
        ...,
        description="Phone number in international or local format.",
        json_schema_extra={"example": "+7 495 123-45-67"},
    )


class OrganizationDTO(BaseModel):
    """
    DTO representing an organization with its facility, phone numbers,
    and associated business types.
    """

    id: UUID = Field(
        ...,
        description="Unique identifier of the organization.",
        json_schema_extra={"example": "99999999-9999-9999-9999-999999999999"},
    )

    name: str = Field(
        ...,
        description="Human-readable name of the organization.",
        json_schema_extra={"example": "Coffee House №1"},
    )

    phones: list[PhoneDTO] = Field(
        ...,
        description="List of phone numbers associated with the organization.",
        json_schema_extra={"example": [{"number": "+7 495 123-45-67"}]},
    )

    facility: FacilityDTO = Field(
        ...,
        description="Facility where the organization is located.",
        json_schema_extra={
            "example": {
                "id": "11111111-1111-1111-1111-111111111111",
                "address": "г. Москва, пр-т Мира 10",
                "lat": "55.790001",
                "lon": "37.630001",
            }
        },
    )

    business_types: list[BusinessTypeDTO] = Field(
        ...,
        description="List of business types describing the organization's activity.",
        json_schema_extra={
            "example": [
                {
                    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                    "name": "Restaurant",
                    "parent_id": None,
                }
            ]
        },
    )

    @staticmethod
    def from_domain(org: Organization):
        return OrganizationDTO(
            id=org.id.value,
            name=org.name.value,
            phones=[PhoneDTO(number=p.value) for p in org.phone_numbers],
            facility=FacilityDTO(
                id=org.facility.id.value,
                address=org.facility.address.address,
                lat=str(org.facility.coordinates.lat),
                lon=str(org.facility.coordinates.lon),
            ),
            business_types=[
                BusinessTypeDTO(
                    id=bt.id.value,
                    name=bt.name.value,
                    parent_id=bt.parent.id.value if bt.parent else None,
                )
                for bt in org.business_types
            ],
        )
