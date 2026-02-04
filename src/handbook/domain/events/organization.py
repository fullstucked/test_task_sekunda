from dataclasses import dataclass

from domain.events.base import DomainEvent
from domain.val_objs.ids import OrganizationId
from domain.val_objs.organization_name import OrganizationName


@dataclass(frozen=True, slots=True)
class OrganizationCreated(DomainEvent):
    organization_id: OrganizationId


@dataclass(frozen=True, slots=True)
class OrganizationNameChanged(DomainEvent):
    organization_id: OrganizationId
    old_name: OrganizationName
    new_name: OrganizationName
