"""Reads transfer requests from JSON files and validates their IBAN codes."""
import json
import re

from bank_manager.transaction_management_exception import TransactionManagementException
from bank_manager.transaction_request import TransactionRequest

SPANISH_IBAN_PATTERN = re.compile(r"ES[0-9]{22}")


class TransactionManager:
    """Loads and validates transaction requests."""

    @staticmethod
    def validate_iban(iban):
        """Return True if `iban` is a valid Spanish IBAN (ISO 13616, mod 97)."""
        if not isinstance(iban, str) or not SPANISH_IBAN_PATTERN.fullmatch(iban):
            return False

        # Move the country code and check digits to the end, replacing the
        # letters by numbers (E = 14, S = 28). The IBAN is valid if the
        # resulting number leaves a remainder of 1 when divided by 97.
        rearranged = iban[4:] + "1428" + iban[2:4]
        return int(rearranged) % 97 == 1

    def read_transaction_from_json(self, file_path):
        """Read a transfer request from a JSON file and validate both IBANs.

        The file must contain the keys "from", "to" and "receptor_name".
        Raises TransactionManagementException if the file cannot be read,
        is not valid JSON, lacks a key or contains an invalid IBAN.
        """
        try:
            with open(file_path, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise TransactionManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise TransactionManagementException("JSON Decode Error - Wrong JSON Format") from ex

        try:
            iban_from = data["from"]
            iban_to = data["to"]
            receptor_name = data["receptor_name"]
        except (KeyError, TypeError) as ex:
            raise TransactionManagementException("JSON Decode Error - Invalid JSON Key") from ex

        if not self.validate_iban(iban_from):
            raise TransactionManagementException("Invalid FROM IBAN")
        if not self.validate_iban(iban_to):
            raise TransactionManagementException("Invalid TO IBAN")
        return TransactionRequest(iban_from, iban_to, receptor_name)
