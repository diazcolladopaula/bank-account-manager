"""Base class for validated values."""
# pylint: disable=too-few-public-methods
import re
from bank_manager import AccountManagementException

class Attribute:
    """A value that must match a regular expression to be valid."""
    def __init__(self):
        self._validation_pattern = r""
        self._error_message = ""
        self._attr_value = ""

    def _validate(self, attr_value):
        """Return `attr_value` if it matches the pattern, else raise an exception."""
        myregex = re.compile(self._validation_pattern)
        regex_matches = myregex.fullmatch(attr_value)
        if not regex_matches:
            raise AccountManagementException(self._error_message)
        return attr_value

    @property
    def value(self):
        """The validated value."""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = self._validate(attr_value)
