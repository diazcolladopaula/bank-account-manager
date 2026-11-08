"""Transfer type."""
from bank_manager.data.attr.attribute import Attribute
# pylint: disable=too-few-public-methods

class TransferType(Attribute):
    """Transfer type: ORDINARY, INMEDIATE or URGENT."""

    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"(ORDINARY|INMEDIATE|URGENT)"
        self._error_message = "Invalid transfer type"
        self._attr_value = self._validate(attr_value)
