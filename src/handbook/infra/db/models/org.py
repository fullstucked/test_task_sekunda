from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base

class OrganizationModel(Base):
    __tablename__ = "organization"
    # __table_args__ = {'extend_existing': True}  # Allow redefinition

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    facility_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("facility.id", ondelete="CASCADE"),
        nullable=False,
    )

    facility: Mapped["FacilityModel"] = relationship(
        back_populates="organizations", lazy="raise"
    )

    phone_numbers: Mapped[List["PhoneModel"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan", lazy="raise"
    )

    activities: Mapped[List["BusinessTypeModel"]] = relationship(
        secondary="organization_business_type",
        back_populates="organizations",
        lazy="raise",
    )
