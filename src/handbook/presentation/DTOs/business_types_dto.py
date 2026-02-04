from uuid import UUID
from pydantic import BaseModel, Field


class BusinessTypeTreeDTO(BaseModel):
    id: UUID = Field(
        ...,
        description="Business type ID.",
        json_schema_extra={"example": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"},
    )
    name: str = Field(
        ...,
        description="Business type name.",
        json_schema_extra={"example": "Food Service"},
    )
    children: list["BusinessTypeTreeDTO"] = Field(
        default_factory=list,
        description="Child business types forming a hierarchy tree.",
    )

    @staticmethod
    def from_domain(bt):
        return BusinessTypeTreeDTO(
            id=bt.id_.value,
            name=bt.name.value,
            children=[BusinessTypeTreeDTO.from_domain(child) for child in bt.children],
        )


class BusinessTypeHierarchyDTO(BaseModel):
    id: UUID = Field(
        ...,
        description="Business type ID.",
        json_schema_extra={"example": "cccccccc-cccc-cccc-cccc-cccccccccccc"},
    )
    name: str = Field(
        ...,
        description="Business type name.",
        json_schema_extra={"example": "Retail"},
    )
    parent_id: UUID | None = Field(
        None,
        description="Parent business type ID, if any.",
        json_schema_extra={"example": None},
    )
    children_ids: list[UUID] = Field(
        ...,
        description="List of child business type IDs.",
        json_schema_extra={"example": ["dddddddd-dddd-dddd-dddd-dddddddddddd"]},
    )

    @staticmethod
    def from_domain(bt):
        return BusinessTypeHierarchyDTO(
            id=bt.id_.value,
            name=bt.name.value,
            parent_id=bt.parent.id_.value if bt.parent else None,
            children_ids=[child.id_.value for child in bt.children],
        )


class BusinessTypeDTO(BaseModel):
    id: UUID = Field(
        ...,
        description="Unique identifier of the business type.",
        json_schema_extra={"example": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"},
    )
    name: str = Field(
        ...,
        description="Name of the business type.",
        json_schema_extra={"example": "Restaurant"},
    )
    parent_id: UUID | None = Field(
        None,
        description="Parent business type ID, if any.",
        json_schema_extra={"example": None},
    )

    @staticmethod
    def from_domain(bt):
        return BusinessTypeDTO(
            id=bt.id_.value,
            name=bt.name.value,
            parent_id=bt.parent.id_.value if bt.parent else None,
        )
