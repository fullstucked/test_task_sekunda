from dataclasses import dataclass

from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class Address(ValueObject):
    """raises DomainTypeError"""

    address: str
