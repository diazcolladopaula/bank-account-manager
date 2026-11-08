"""Transfer amount."""
from bank_manager import AccountManagementException
from bank_manager.data.attr.attribute import Attribute


class TransferAmount(Attribute):
    """Transfer amount: a number from 10 to 10000 with at most two decimals."""
    def __init__(self, amount_value):
        super().__init__()
        self._error_message = "Invalid transfer amount"
        self._attr_value = self.validate(amount_value)

    def validate(self, attr_value):
        """Check that the amount is a number in range with at most two decimals."""
        try:
            amount_float = float(attr_value)
        except ValueError as exc:
            raise AccountManagementException(self._error_message) from exc
        str_amount = str(amount_float)
        if '.' in str_amount:
            decimals = len(str_amount.split('.')[1])
            if decimals > 2:
                raise AccountManagementException(self._error_message)
        if amount_float < 10 or amount_float > 10000:
            raise AccountManagementException(self._error_message)
        return attr_value
