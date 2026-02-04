from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base

class BusinessTypeModel(Base):
    __tablename__ = "business_type"
    __table_args__ = (
        UniqueConstraint("parent_id", "name"),
        Index("ix_business_type_parent", "parent_id"),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_type.id", ondelete="CASCADE"),
        nullable=True,
    )

    parent: Mapped["BusinessTypeModel"] = relationship(
        back_populates="children", remote_side=[id]
    )

    children: Mapped[list["BusinessTypeModel"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )

    descendants: Mapped[list["BusinessTypeClosureModel"]] = relationship(
        back_populates="ancestor",
        cascade="all, delete-orphan",
        foreign_keys="BusinessTypeClosureModel.ancestor_id",
    )

    ancestors: Mapped[list["BusinessTypeClosureModel"]] = relationship(
        back_populates="descendant",
        cascade="all, delete-orphan",
        foreign_keys="BusinessTypeClosureModel.descendant_id",
    )

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        secondary="organization_business_type", back_populates="activities"
    )
