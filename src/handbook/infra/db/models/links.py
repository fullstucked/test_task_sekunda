from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from infra.db.base import Base

organization_business_type = Table(
    "organization_business_type",
    Base.metadata,
    Column(
        "organization_id",
        UUID(as_uuid=True),
        ForeignKey("organization.id"),
        primary_key=True,
    ),
    Column(
        "business_type_id",
        UUID(as_uuid=True),
        ForeignKey("business_type.id"),
        primary_key=True,
    ),
)
