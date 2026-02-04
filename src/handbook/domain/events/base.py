from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """
    Base class for all domain events.
    """
    context: dict[str, Any] = field(default_factory=dict, init=False)
    # occurred_at: datetime = field(default_factory=datetime.utcnow, init=False)

    def __init__(self, *args, **kwargs):
        object.__setattr__(self, 'context', kwargs.get('context', {}))
        # object.__setattr__(self, 'occurred_at', datetime.utcnow())
