import re
from dataclasses import dataclass, field
from typing import ClassVar

from domain.exceptions.base import DomainTypeError
from domain.exceptions.org_err import InvalidPhoneNumberError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class PhoneNumber(ValueObject):
    value: str = field(repr=True)

    MIN_LEN: ClassVar[int] = 6
    MAX_LEN: ClassVar[int] = 25

    PATTERN_START = re.compile(r"^[0-9+]")
    PATTERN_ALLOWED_CHARS = re.compile(r"[0-9+\-]*")

    def __post_init__(self) -> None:
        self._validate_length(self.value)
        self._validate_pattern(self.value)

    def _validate_length(self, v: str) -> None:
        if not (self.MIN_LEN <= len(v) <= self.MAX_LEN):
            raise DomainTypeError(
                f"Phone number must be {self.MIN_LEN}–{self.MAX_LEN} characters"
            )

    def _validate_pattern(self, v: str) -> None:
        if not self.PATTERN_START.match(v):
            raise InvalidPhoneNumberError(
                phone_number=self.value,
                reason="Phone number must start with a digit or +",
            )
        if not self.PATTERN_ALLOWED_CHARS.fullmatch(v):
            raise InvalidPhoneNumberError(
                phone_number=self.value,
                reason="Phone number contains invalid characters",
            )
