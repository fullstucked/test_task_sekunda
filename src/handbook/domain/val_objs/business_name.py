from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import ClassVar, Final

from domain.exceptions.business_type_err import BusinessTypeTypeError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class BusinessName(ValueObject):
    value: str = field(repr=True)

    MIN_LEN: ClassVar[Final[int]] = 4
    MAX_LEN: ClassVar[Final[int]] = 100

    ALLOWED_CHARS = r"a-zA-ZА-Яа-яЁё0-9._\-\"'`«»“”‘’"
    PATTERN_START = re.compile(r"^[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]")
    PATTERN_ALLOWED_CHARS = re.compile(rf"[{ALLOWED_CHARS}]*")
    PATTERN_NO_CONSECUTIVE_SPECIALS = re.compile(
        r"^[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]+([._\-\"'`«»“”‘’]?[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]+)*[._\-\"'`«»“”‘’]?$"
    )
    PATTERN_END = re.compile(r".*[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]$")

    def __post_init__(self) -> None:
        self._validate_length(self.value)

        ### Depends on requirements and real-life obstacles, patterns should be changed and validation turned on
        # self._validate_pattern(self.value)
        ###


    def _validate_length(self, v: str) -> None:
        if not (self.MIN_LEN <= len(v) <= self.MAX_LEN):
            raise BusinessTypeTypeError(
                f"Business type name must be {self.MIN_LEN}–{self.MAX_LEN} characters"
            )

    def _validate_pattern(self, v: str) -> None:
        if not self.PATTERN_START.match(v):
            raise BusinessTypeTypeError(
                "Business type must start with a letter or digit"
            )

        if not self.PATTERN_ALLOWED_CHARS.fullmatch(v):
            raise BusinessTypeTypeError("Business type contains invalid characters")

        if not self.PATTERN_NO_CONSECUTIVE_SPECIALS.fullmatch(v):
            raise BusinessTypeTypeError(
                "Business type contains invalid character sequences"
            )

        if not self.PATTERN_END.match(v):
            raise BusinessTypeTypeError("Business type must end with a letter or digit")
