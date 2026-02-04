from dataclasses import dataclass, fields
from typing import Any, Self


@dataclass(frozen=True, slots=True, repr=False)
class ValueObject:
    """
    Base class for immutable value objects (VO) in domain.
    Defined by instance attributes only; these must be immutable.

    Repr policy: `__repr__` includes only fields with `repr=True`;
    fields with `repr=False` are omitted to avoid leaking secrets.
    If no fields have `repr=True`, '<hidden>' is shown.
    """

    def __new__(cls, *_args: Any, **_kwargs: Any) -> Self:
        if cls is ValueObject:
            raise TypeError("Base ValueObject cannot be instantiated directly.")
        if not fields(cls):
            raise TypeError(f"{cls.__name__} must have at least one field!")
        return object.__new__(cls)

    def __post_init__(self) -> None:
        # Ensure subclass has fields
        if not fields(self):
            raise TypeError(f"{type(self).__name__} must define at least one field")

        # Ensure all fields are immutable
        for f in fields(self):
            value = getattr(self, f.name)
            if self._is_mutable(value):
                raise TypeError(
                    f"Field '{f.name}' in {type(self).__name__} must be immutable, "
                    f"got {type(value).__name__}"
                )

    @staticmethod
    def _is_mutable(value: Any) -> bool:
        """Detect mutable types."""
        return isinstance(value, (list, dict, set, bytearray))

    def __repr__(self) -> str:
        items = [f for f in fields(self) if f.repr]
        if not items:
            return f"{type(self).__name__}(<hidden>)"
        if len(items) == 1:
            f = items[0]
            return f"{type(self).__name__}({getattr(self, f.name)!r})"
        return (
            f"{type(self).__name__}("
            + ", ".join(f"{f.name}={getattr(self, f.name)!r}" for f in items)
            + ")"
        )
