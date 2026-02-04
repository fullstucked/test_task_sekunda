from decimal import Decimal
from pydantic import BaseModel, Field


class ProximityQuery(BaseModel):
    """Query parameters for proximity-based search."""

    lat: Decimal = Field(
        ...,
        description="Latitude of the center point.",
        json_schema_extra={"example": "55.790001"},
    )

    lon: Decimal = Field(
        ...,
        description="Longitude of the center point.",
        json_schema_extra={"example": "37.630001"},
    )

    radius_meters: float = Field(
        ...,
        description="Search radius in meters.",
        json_schema_extra={"example": 2000.20},
    )
