from decimal import Decimal

from pydantic import BaseModel, Field


class RectangleQuery(BaseModel):
    """Query parameters for rectangle-based geospatial search."""

    lat1: Decimal = Field(
        ...,
        description="Latitude of the first corner of the rectangle.",
        json_schema_extra={"example": "55.7890"},
    )

    lon1: Decimal = Field(
        ...,
        description="Longitude of the first corner of the rectangle.",
        json_schema_extra={"example": "37.6290"},
    )

    lat2: Decimal = Field(
        ...,
        description="Latitude of the opposite corner of the rectangle.",
        json_schema_extra={"example": "55.7910"},
    )

    lon2: Decimal = Field(
        ...,
        description="Longitude of the opposite corner of the rectangle.",
        json_schema_extra={"example": "37.6310"},
    )
