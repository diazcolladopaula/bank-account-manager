"""Deposit amount."""
from bank_manager import AccountManagementException
from bank_manager.data.attr.attribute import Attribute


class DepositAmount(Attribute):
    """Deposit amount written as "EUR 0000.00"; its value is the number as a float."""
    def __init__(self, deposit_amount_value):
        super().__init__()
        self._validation_pattern = r"^EUR [0-9]{4}\.[0-9]{2}"
        self._error_message = "Error - Invalid deposit amount"
        self._attr_value = self.validate(deposit_amount_value)

    def validate(self, attr_value):
        """Check the format and that the amount is not zero."""
        super()._validate(attr_value)
        amount_float = float(attr_value[4:])
        if amount_float == 0:
            raise AccountManagementException("Error - Deposit must be greater than 0")
        return amount_float
