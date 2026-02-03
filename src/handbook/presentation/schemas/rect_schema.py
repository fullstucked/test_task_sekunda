from decimal import Decimal

from pydantic import BaseModel, Field


class RectangleQuery(BaseModel):
    """Query parameters for rectangle-based geospatial search."""

    lat1: Decimal = Field(
        ...,
        description="Latitude of the first corner of the rectangle.",
        example="55.7890",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
    lon1: Decimal = Field(
        ...,
        description="Longitude of the first corner of the rectangle.",
        example="37.6290",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
    lat2: Decimal = Field(
        ...,
        description="Latitude of the opposite corner of the rectangle.",
        example="55.7910",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
    lon2: Decimal = Field(
        ...,
        description="Longitude of the opposite corner of the rectangle.",
        example="37.6310",
        #pattern=r"^-?\d{1,3}\.\d{1,15}$",
    )
