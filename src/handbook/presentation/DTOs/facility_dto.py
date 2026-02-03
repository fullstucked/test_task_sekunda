from uuid import UUID

from pydantic import BaseModel, Field


class FacilityDTO(BaseModel):
    id: UUID = Field(
        ...,
        description="Unique identifier of the facility.",
        example="11111111-1111-1111-1111-111111111111",
    )
    address: str = Field(
        ...,
        description="Human-readable address of the facility.",
        example="г. Москва, пр-т Мира 10",
    )
    lat: str = Field(
        ...,
        description="Latitude of the facility as a string.",
        example="55.790001",
    )
    lon: str = Field(
        ...,
        description="Longitude of the facility as a string.",
        example="37.630001",
    )

    @staticmethod
    def from_domain(facility):
        return FacilityDTO(
            id=facility.id_.value,
            address=facility.address.address,
            lat=str(facility.coordinates.lat),
            lon=str(facility.coordinates.lon),
        )
