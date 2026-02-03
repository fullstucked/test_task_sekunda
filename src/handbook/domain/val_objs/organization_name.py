import re
from dataclasses import dataclass
from typing import ClassVar, Final

from domain.exceptions.org_err import OrganizationTypeError
from domain.val_objs.base import ValueObject


@dataclass(frozen=True, slots=True, repr=False)
class OrganizationName(ValueObject):
    """raises OrganizationTypeError"""

    MIN_LEN: ClassVar[Final[int]] = 5
    MAX_LEN: ClassVar[Final[int]] = 20
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
        """:raises OrganizationTypeError:"""
        self._validate_org_name_length(self.value)
        # self._validate_org_name_pattern(self.value)

    def _validate_org_name_length(self, org_name_value: str) -> None:
        """:raises OrganizationTypeError:"""
        if len(org_name_value) < self.MIN_LEN or len(org_name_value) > self.MAX_LEN:
            raise OrganizationTypeError(
                f"org_ must be between {self.MIN_LEN} and {self.MAX_LEN} characters.",
            )

    def _validate_org_name_pattern(self, org_name_value: str) -> None:
        """:raises OrganizationTypeError:"""
        if not re.match(self.PATTERN_START, org_name_value):
            raise OrganizationTypeError(
                "org_ must start with a letter (A-Z, a-z) or a digit (0-9).",
            )
        if not re.fullmatch(self.PATTERN_ALLOWED_CHARS, org_name_value):
            raise OrganizationTypeError(
                "org_ can only contain letters (A-Z, a-z), digits (0-9), "
                "dots (.), hyphens (-), and underscores (_).",
            )
        if not re.fullmatch(self.PATTERN_NO_CONSECUTIVE_SPECIALS, org_name_value):
            raise OrganizationTypeError(
                "org_ cannot contain consecutive special characters"
                " like .., --, or __.",
            )
        if not re.match(self.PATTERN_END, org_name_value):
            raise OrganizationTypeError(
                "org_ must end with a letter (A-Z, a-z) or a digit (0-9).",
            )
