"""Transfer concept."""
# pylint: disable=too-few-public-methods
from bank_manager.data.attr.attribute import Attribute


class Concept(Attribute):
    """Concept: 10 to 30 letters, in at least two words separated by single spaces."""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^(?=^.{10,30}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid concept format"
        self._attr_value = self._validate(attr_value)
