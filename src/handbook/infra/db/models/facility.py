from __future__ import annotations

import uuid

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base


class FacilityModel(Base):
    __tablename__ = "facility"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    address: Mapped[str] = mapped_column(String(255), nullable=False)
    lat: Mapped[str] = mapped_column(String, nullable=True)
    lon: Mapped[str] = mapped_column(String, nullable=True)

    organizations: Mapped[list["OrganizationModel"]] = relationship(
        back_populates="facility", lazy="raise"
    )
