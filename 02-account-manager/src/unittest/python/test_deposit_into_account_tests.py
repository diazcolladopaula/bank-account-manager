"""Tests for AccountManager.deposit_into_account."""
import json
import os
import tempfile
import unittest

from bank_manager import AccountManager, AccountManagementException

IBAN = "ES9121000418450200051332"


class TestDeposit(unittest.TestCase):
    """Deposit files with valid and invalid contents."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data_dir = tmp.name
        self.file_name = os.path.join(tmp.name, "deposit.json")
        self.manager = AccountManager(data_dir=self.data_dir)

    def write(self, content):
        """Write `content` (dict or raw text) to the deposit file."""
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.write(content if isinstance(content, str) else json.dumps(content))

    def assert_error(self, content, message):
        """The deposit file with `content` must be rejected with `message`."""
        self.write(content)
        with self.assertRaises(AccountManagementException) as context:
            self.manager.deposit_into_account(self.file_name)
        self.assertEqual(context.exception.message, message)

    def test_valid_deposits(self):
        """Valid amounts return a 64-character SHA-256 signature."""
        cases = {"TCV1": "EUR 100.00", "TCV2": "EUR 0.01", "TCV3": "EUR 999999999.99",
                 "TCV4": "EUR 123.45", "TCV5": "EUR 123.4"}
        for case_id, amount in cases.items():
            with self.subTest(case_id):
                self.write({"IBAN": IBAN, "AMOUNT": amount})
                signature = self.manager.deposit_into_account(self.file_name)
                self.assertIsInstance(signature, str)
                self.assertEqual(len(signature), 64)

    def test_deposits_are_stored(self):
        """Each accepted deposit is appended to deposits.json."""
        self.write({"IBAN": IBAN, "AMOUNT": "EUR 50.00"})
        first = self.manager.deposit_into_account(self.file_name)
        second = self.manager.deposit_into_account(self.file_name)
        with open(os.path.join(self.data_dir, "deposits.json"), encoding="utf-8") as file:
            stored = json.load(file)
        self.assertEqual(len(stored), 2)
        self.assertEqual(stored[0]["deposit_signature"], first)
        self.assertEqual(stored[1]["deposit_signature"], second)
        self.assertEqual(stored[0]["to_iban"], IBAN)
        self.assertEqual(stored[0]["deposit_amount"], 50.0)

    def test_invalid_structure(self):
        """Missing, extra or misspelled keys are rejected."""
        cases = {
            "TCNV1": {"AMOUNT": "EUR 100.00"},
            "TCNV2": {"IBAN": IBAN},
            "TCNV10": {"{IBAN": IBAN, "AMOUNT": "EUR 123"},
            "TCNV18": {"IBANIBAN": IBAN, "AMOUNT": "EUR 100.50"},
            "TCNV19": {"": IBAN, "AMOUNT": "EUR 100.50"},
            "TCNV20": {"aa": IBAN, "AMOUNT": "EUR 100.50"},
            "TCNV21": {"IBAN": IBAN, "AMOUNTAMOUNT": "EUR 100.50"},
            "TCNV22": {"IBAN": IBAN, "": "EUR 100.50"},
            "TCNV23": {"IBAN": IBAN, "aa": "EUR 100.50"},
            "extra key": {"IBAN": IBAN, "AMOUNT": "EUR 1.00", "NOTE": "x"},
            "amount not a string": {"IBAN": IBAN, "AMOUNT": 100},
            "not an object": [IBAN, "EUR 100.00"],
        }
        for case_id, content in cases.items():
            with self.subTest(case_id):
                self.assert_error(content, "Invalid JSON format")

    def test_invalid_iban(self):
        """IBAN with the wrong country, length or check digits are rejected."""
        cases = {
            "TCNV3": "GB29NWBK60161331926819",
            "TCNV4": IBAN[:-1],
            "TCNV5": IBAN + "4",
            "TCNV12": IBAN + "IBAN:" + IBAN,
            "wrong check digits": "ES9021000418450200051332",
            "not a string": 12345,
        }
        for case_id, iban in cases.items():
            with self.subTest(case_id):
                self.assert_error({"IBAN": iban, "AMOUNT": "EUR 100.00"}, "Invalid IBAN")

    def test_invalid_currency(self):
        """Only euro amounts are accepted."""
        self.assert_error({"IBAN": IBAN, "AMOUNT": "USD 100.00"}, "Invalid currency")

    def test_non_numeric_amount(self):
        """The part after the currency must be a number."""
        cases = {"TCNV7": "EUR one hundred", "TCNV15": "EUR 123AMOUNT: EUR 123",
                 "TCNV16": 'EUR 123"', "empty": "EUR "}
        for case_id, amount in cases.items():
            with self.subTest(case_id):
                self.assert_error({"IBAN": IBAN, "AMOUNT": amount}, "Non-numeric amount")

    def test_invalid_amount(self):
        """Zero, negative and non-finite amounts are rejected."""
        cases = {"TCNV8": "EUR 0.00", "TCNV9": "EUR -1.00",
                 "nan": "EUR nan", "infinity": "EUR inf"}
        for case_id, amount in cases.items():
            with self.subTest(case_id):
                self.assert_error({"IBAN": IBAN, "AMOUNT": amount}, "Invalid amount")

    def test_file_errors(self):
        """Missing and malformed files are reported."""
        with self.assertRaises(AccountManagementException) as context:
            self.manager.deposit_into_account(os.path.join(self.data_dir, "missing.json"))
        self.assertEqual(context.exception.message, "File not found")
        self.assert_error("{not json", "Invalid JSON file")


if __name__ == "__main__":
    unittest.main()
