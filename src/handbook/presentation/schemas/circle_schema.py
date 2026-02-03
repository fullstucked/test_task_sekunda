from decimal import Decimal

from pydantic import BaseModel, Field


class ProximityQuery(BaseModel):
    """Query parameters for proximity-based search."""

    lat: Decimal = Field(
        ...,
        description="Latitude of the center point.",
        example="55.790001",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
    lon: Decimal = Field(
        ...,
        description="Longitude of the center point.",
        example="37.630001",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
    radius_meters: float = Field(
        ...,
        description="Search radius in meters.",
        example=2000.20,
    )
