from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base


class PhoneModel(Base):
    __tablename__ = "phone_table"

    phone_number: Mapped[str] = mapped_column(String(50), primary_key=True)

    org_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("organization.id", ondelete="CASCADE")
    )

    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="phone_numbers", lazy="raise"
    )
