from uuid import UUID

from pydantic import BaseModel, Field


class BusinessTypeTreeDTO(BaseModel):
    id: UUID = Field(
        ...,
        description="Business type ID.",
        example="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
    )
    name: str = Field(
        ...,
        description="Business type name.",
        example="Food Service",
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
        example="cccccccc-cccc-cccc-cccc-cccccccccccc",
    )
    name: str = Field(
        ...,
        description="Business type name.",
        example="Retail",
    )
    parent_id: UUID | None = Field(
        None,
        description="Parent business type ID, if any.",
        example=None,
    )
    children_ids: list[UUID] = Field(
        ...,
        description="List of child business type IDs.",
        example=["dddddddd-dddd-dddd-dddd-dddddddddddd"],
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
        example="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    )
    name: str = Field(
        ...,
        description="Name of the business type.",
        example="Restaurant",
    )
    parent_id: UUID | None = Field(
        None,
        description="Parent business type ID, if any.",
        example=None,
    )

    @staticmethod
    def from_domain(bt):
        return BusinessTypeDTO(
            id=bt.id_.value,
            name=bt.name.value,
            parent_id=bt.parent.id_.value if bt.parent else None,
        )
