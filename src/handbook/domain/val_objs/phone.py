import re
from dataclasses import dataclass
from typing import ClassVar, Final

from domain.exceptions.base import DomainTypeError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class PhoneNumber(ValueObject):
    """raises DomainTypeError"""

    MIN_LEN: ClassVar[Final[int]] = 6
    MAX_LEN: ClassVar[Final[int]] = 25

    # Pattern for validating a phone`:
    # - starts with a letter (A-Z, a-z) or a digit (0-9)
    PATTERN_START: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"^[0-9+]",
    )
    # - can contain multiple special characters . - _ between letters and digits,
    PATTERN_ALLOWED_CHARS: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"[0-9+-]*",
    )

    value: str

    def __post_init__(self) -> None:
        """:raises DomainTypeError:"""
        self._validate_phone_length(self.value)
        # self._validate_phone_pattern(self.value)

    def _validate_phone_length(self, phone_value: str) -> None:
        """:raises DomainTypeError:"""
        if len(phone_value) < self.MIN_LEN or len(phone_value) > self.MAX_LEN:
            raise DomainTypeError(
                f"Phone number must be between {self.MIN_LEN} and {self.MAX_LEN} characters.",
            )

    def _validate_phone_pattern(self, phone_value: str) -> None:
        """:raises DomainTypeError:"""
        if not re.match(self.PATTERN_START, phone_value):
            raise DomainTypeError(
                "Phone number must start with a letter (A-Z, a-z) or a digit (0-9).",
            )
        if not re.fullmatch(self.PATTERN_ALLOWED_CHARS, phone_value):
            raise DomainTypeError(
                "Phone number can only contain letters (A-Z, a-z), digits (0-9), "
                "dots (.), hyphens (-), and underscores (_).",
            )
