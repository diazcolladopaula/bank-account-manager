"""Account manager: transfer requests, deposits and balance calculation."""
# pylint: disable=too-many-arguments
import json
import math
import re
from datetime import datetime
from pathlib import Path

from .account_deposit import AccountDeposit
from .account_management_exception import AccountManagementException
from .transfer_request import TransferRequest

TRANSFERS_FILE = "transfers.json"
DEPOSITS_FILE = "deposits.json"
TRANSACTIONS_FILE = "all_transactions.json"

IBAN_PATTERN = re.compile(r"ES[0-9]{22}")
CONCEPT_PATTERN = re.compile(r"[A-Za-z0-9 ]{10,30}")
TRANSFER_TYPES = {"ORDINARY", "URGENT", "IMMEDIATE"}


class AccountManager:
    """Validates and stores transfers and deposits, and computes balances.

    All data is read from and written to JSON files inside `data_dir`
    (by default a `data` folder in the current working directory).
    """

    def __init__(self, data_dir=None):
        self._data_dir = Path(data_dir) if data_dir is not None else Path("data")

    # ---- validation -------------------------------------------------------

    @staticmethod
    def validate_iban(iban):
        """Return True if `iban` is a valid Spanish IBAN (24 characters, mod 97)."""
        if not isinstance(iban, str) or not IBAN_PATTERN.fullmatch(iban):
            return False
        # Move the first four characters to the end and turn letters into
        # numbers (A=10 ... Z=35). The IBAN is valid if the result is 1 mod 97.
        rearranged = iban[4:] + iban[:4]
        numeric = "".join(str(int(char, 36)) for char in rearranged)
        return int(numeric) % 97 == 1

    @staticmethod
    def validate_concept(concept):
        """A concept has 10 to 30 letters, digits or spaces, with at least one space."""
        return (isinstance(concept, str)
                and CONCEPT_PATTERN.fullmatch(concept) is not None
                and " " in concept)

    @staticmethod
    def validate_transfer_type(transfer_type):
        """The transfer type must be ORDINARY, URGENT or IMMEDIATE."""
        return transfer_type in TRANSFER_TYPES

    @staticmethod
    def validate_date(date):
        """The date must be dd/mm/yyyy, today or later, and between 2025 and 2050."""
        try:
            parsed = datetime.strptime(date, "%d/%m/%Y")
        except (ValueError, TypeError):
            return False
        return 2025 <= parsed.year <= 2050 and parsed.date() >= datetime.today().date()

    @staticmethod
    def validate_amount(amount):
        """The amount must be a number from 10.00 to 10000.00 with at most 2 decimals."""
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            return False
        return 10.00 <= amount <= 10000.00 and round(amount, 2) == amount

    # ---- file helpers -----------------------------------------------------

    def _read_list(self, file_name, error_message):
        """Return the JSON list stored in `file_name` ([] if it does not exist yet)."""
        try:
            with open(self._data_dir / file_name, encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as ex:
            raise AccountManagementException(error_message) from ex

    def _write_list(self, file_name, items):
        self._data_dir.mkdir(parents=True, exist_ok=True)
        with open(self._data_dir / file_name, "w", encoding="utf-8") as file:
            json.dump(items, file, indent=4)

    # ---- operations -------------------------------------------------------

    def transfer_request(self, from_iban, to_iban, concept, transfer_type, date, amount):
        """Validate a transfer, store it and return its transfer code.

        Raises AccountManagementException if any field is invalid or if the
        same transfer has already been stored.
        """
        if not self.validate_iban(from_iban):
            raise AccountManagementException("from_iban not valid")
        if not self.validate_concept(concept):
            raise AccountManagementException("Invalid transfer concept")
        if not self.validate_transfer_type(transfer_type):
            raise AccountManagementException("transfer type is not valid")
        if not self.validate_date(date):
            raise AccountManagementException("date not valid")
        if not self.validate_amount(amount):
            raise AccountManagementException("amount not valid")
        if not self.validate_iban(to_iban):
            raise AccountManagementException("to_iban not valid")

        transfer = TransferRequest(from_iban=from_iban,
                                   transfer_type=transfer_type,
                                   to_iban=to_iban,
                                   transfer_concept=concept,
                                   transfer_date=date,
                                   transfer_amount=amount)
        record = transfer.to_json()

        transfers = self._read_list(TRANSFERS_FILE, "transfers file is not a valid JSON")
        if record in transfers:
            raise AccountManagementException("Duplicate transfer")
        transfers.append(record)
        self._write_list(TRANSFERS_FILE, transfers)
        return transfer.transfer_code

    def deposit_into_account(self, input_file):
        """Read a deposit from a JSON file, store it and return its signature.

        The file must contain exactly the keys "IBAN" and "AMOUNT", where the
        amount has the form "EUR <positive number>".
        """
        try:
            with open(input_file, encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise AccountManagementException("File not found") from ex
        except json.JSONDecodeError as ex:
            raise AccountManagementException("Invalid JSON file") from ex

        if (not isinstance(data, dict) or set(data) != {"IBAN", "AMOUNT"}
                or not isinstance(data["AMOUNT"], str)):
            raise AccountManagementException("Invalid JSON format")
        iban = data["IBAN"]
        amount_text = data["AMOUNT"]

        if not self.validate_iban(iban):
            raise AccountManagementException("Invalid IBAN")
        if not amount_text.startswith("EUR "):
            raise AccountManagementException("Invalid currency")
        try:
            amount = float(amount_text[4:])
        except ValueError as ex:
            raise AccountManagementException("Non-numeric amount") from ex
        if not math.isfinite(amount) or amount <= 0:
            raise AccountManagementException("Invalid amount")

        deposit = AccountDeposit(iban, amount)
        deposits = self._read_list(DEPOSITS_FILE, "deposits file is not a valid JSON")
        deposits.append(deposit.to_json())
        self._write_list(DEPOSITS_FILE, deposits)
        return deposit.deposit_signature

    def calculate_balance(self, iban):
        """Add up all the transactions of `iban` and store the result.

        The balance is written to `<iban>.json` in the data directory.
        Raises AccountManagementException if the IBAN is invalid or has no
        transactions.
        """
        if not self.validate_iban(iban):
            raise AccountManagementException("InvalidIBANCode")
        transactions = self._read_list(TRANSACTIONS_FILE,
                                       "File all_transactions is not a valid JSON")
        amounts = [float(transaction["amount"])
                   for transaction in transactions if transaction["IBAN"] == iban]
        if not amounts:
            raise AccountManagementException("InvalidIBANCode")

        balance = {"iban": iban, "date": str(datetime.now()), "balance": sum(amounts)}
        self._data_dir.mkdir(parents=True, exist_ok=True)
        with open(self._data_dir / f"{iban}.json", "w", encoding="utf-8") as file:
            json.dump(balance, file, indent=4)
        return True
