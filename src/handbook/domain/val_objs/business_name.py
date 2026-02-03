import re
from dataclasses import dataclass
from typing import ClassVar, Final

from domain.exceptions.business_type_err import BusinessTypeTypeError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class BusinessName(ValueObject):
    """raises BusinessTypeTypeError"""

    MIN_LEN: ClassVar[Final[int]] = 5
    MAX_LEN: ClassVar[Final[int]] = 100

    # Allowed characters: Latin, Cyrillic, digits, . _ - and quotes
    ALLOWED_CHARS = r"a-zA-ZА-Яа-яЁё0-9._\-\"'`«»“”‘’"

    # Starts with allowed letter or digit
    PATTERN_START = re.compile(r"^[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]")

    # Allowed characters anywhere
    PATTERN_ALLOWED_CHARS = re.compile(rf"[{ALLOWED_CHARS}]*")

    # No consecutive special characters (. _ - " ' ` « » “ ” ‘ ’)
    PATTERN_NO_CONSECUTIVE_SPECIALS = re.compile(
        r"^[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]+([._\-\"'`«»“”‘’]?[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]+)*[._\-\"'`«»“”‘’]?$"
    )

    # Ends with allowed letter or digit or quote
    PATTERN_END = re.compile(r".*[a-zA-ZА-Яа-яЁё0-9\"'`«»“”‘’]$")
    value: str

    def __post_init__(self) -> None:
        """:raises BusinessTypeTypeError:"""
        self._validate_business_name_length(self.value)
        # TODO
        # self._validate_business_name_pattern(self.value)

    def _validate_business_name_length(self, business_name_value: str) -> None:
        """:raises BusinessTypeTypeError:"""
        if (
            len(business_name_value) < self.MIN_LEN
            or len(business_name_value) > self.MAX_LEN
        ):
            raise BusinessTypeTypeError(
                f"BusinessType name must be between {self.MIN_LEN} and {self.MAX_LEN} characters.",
            )

    def _validate_business_name_pattern(self, business_name_value: str) -> None:
        """:raises BusinessTypeTypeError:"""
        if not re.match(self.PATTERN_START, business_name_value):
            raise BusinessTypeTypeError(
                "Business type must start with a letter (A-Z, a-z) or a digit (0-9).",
            )
        if not re.fullmatch(self.PATTERN_ALLOWED_CHARS, business_name_value):
            raise BusinessTypeTypeError(
                "Business type can only contain letters (A-Z, a-z), digits (0-9), "
                "dots (.), hyphens (-), and underscores (_).",
            )
        if not re.fullmatch(self.PATTERN_NO_CONSECUTIVE_SPECIALS, business_name_value):
            raise BusinessTypeTypeError(
                "Business type cannot contain consecutive special characters"
                " like .., --, or __.",
            )
        if not re.match(self.PATTERN_END, business_name_value):
            raise BusinessTypeTypeError(
                "Business type must end with a letter (A-Z, a-z) or a digit (0-9).",
            )
