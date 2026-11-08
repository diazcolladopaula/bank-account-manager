"""Transfer date."""
# pylint: disable=too-few-public-methods
from datetime import datetime, timezone
from bank_manager import AccountManagementException
from bank_manager.data.attr.attribute import Attribute


class TransferDate(Attribute):
    """Date as dd/mm/yyyy, today or later, between 2025 and 2050."""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._error_message = "Invalid date format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """calls the superclass validation for checking the regex and validate the date according
        the range of allowed years and the python's date definition"""
        attr_value = super()._validate(attr_value)

        try:
            date_obj = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise AccountManagementException("Invalid date format") from ex

        if date_obj < datetime.now(timezone.utc).date():
            raise AccountManagementException("Transfer date must be today or later.")

        if date_obj.year < 2025 or date_obj.year > 2050:
            raise AccountManagementException("Invalid date format")
        return attr_value
