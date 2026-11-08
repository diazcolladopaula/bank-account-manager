"""Balance of an IBAN computed from the transactions file."""
import json
from datetime import datetime, timezone

from bank_manager import AccountManagementException, TRANSACTIONS_STORE_FILE
from bank_manager.data.attr.iban_code import IbanCode


class IbanBalance:
    """Balance of an account at the moment it is created."""
    def __init__(self, iban):
        self._iban = IbanCode(iban).value
        self.__last_balance_time = datetime.timestamp(datetime.now(timezone.utc))
        self.__balance = self.calculate_iban_balance()

    def calculate_iban_balance(self):
        """Add up the amounts of every transaction of this IBAN."""
        transactions_list = self.read_transactions_file()
        iban_found = False
        current_balance = 0
        for transaction in transactions_list:
            if transaction["IBAN"] == self._iban:
                current_balance += float(transaction["amount"])
                iban_found = True
        if not iban_found:
            raise AccountManagementException("IBAN not found")
        return current_balance

    @staticmethod
    def read_transactions_file():
        """Return the list of transactions stored in the transactions file."""
        try:
            with open(TRANSACTIONS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                input_list = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return input_list

    def to_json(self):
        """Return the balance as a JSON-serialisable dict."""
        return {"IBAN": self._iban,
                "time": self.__last_balance_time,
                "BALANCE": self.__balance}
