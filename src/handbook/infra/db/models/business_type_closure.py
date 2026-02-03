import uuid

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base


class BusinessTypeClosureModel(Base):
    __tablename__ = "business_type_closure"

    # __table_args__ = {'extend_existing': True}  # Allow redefinition
    ancestor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_type.id", ondelete="CASCADE"),
        primary_key=True,
    )

    descendant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("business_type.id", ondelete="CASCADE"),
        primary_key=True,
    )

    depth: Mapped[int] = mapped_column(Integer, nullable=False)

    ancestor: Mapped["BusinessTypeModel"] = relationship(
        foreign_keys=[ancestor_id], back_populates="descendants"
    )

    descendant: Mapped["BusinessTypeModel"] = relationship(
        foreign_keys=[descendant_id], back_populates="ancestors"
    )
