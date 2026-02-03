from pydantic import BaseModel, Field


class SearchByNameQuery(BaseModel):
    """Query parameters for searching organizations by name."""

    q: str = Field(
        ...,
        description="Substring to search for in organization names.",
        example="coffee",
    )
