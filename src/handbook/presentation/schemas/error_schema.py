from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response returned by the API."""

    detail: str = Field(
        ...,
        description="Human-readable error message.",
        example="Facility not found",
    )
