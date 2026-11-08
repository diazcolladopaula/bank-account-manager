"""Unit tests for TransactionManager."""
import json
import tempfile
import unittest
from pathlib import Path

from bank_manager import TransactionManager, TransactionManagementException

VALID_FROM = "ES9121000418450200051332"
VALID_TO = "ES7921000813610123456789"


class TestValidateIban(unittest.TestCase):
    """Checks on IBAN validation."""

    def test_valid_ibans(self):
        """Well-formed IBAN with correct check digits are accepted."""
        self.assertTrue(TransactionManager.validate_iban(VALID_FROM))
        self.assertTrue(TransactionManager.validate_iban(VALID_TO))

    def test_wrong_check_digits(self):
        """Changing the check digits makes the IBAN invalid."""
        self.assertFalse(TransactionManager.validate_iban("ES9221000418450200051332"))

    def test_wrong_body(self):
        """Changing one digit of the account number makes the IBAN invalid."""
        self.assertFalse(TransactionManager.validate_iban("ES9121000418450200051333"))

    def test_wrong_length(self):
        """IBAN that are too short or too long are rejected."""
        self.assertFalse(TransactionManager.validate_iban(VALID_FROM[:-1]))
        self.assertFalse(TransactionManager.validate_iban(VALID_FROM + "0"))

    def test_wrong_country(self):
        """Only Spanish IBAN are accepted."""
        self.assertFalse(TransactionManager.validate_iban("FR" + VALID_FROM[2:]))

    def test_non_digit_characters(self):
        """Letters after the country code are rejected."""
        self.assertFalse(TransactionManager.validate_iban("ES91A1000418450200051332"))

    def test_non_string(self):
        """Values that are not strings are rejected instead of raising."""
        self.assertFalse(TransactionManager.validate_iban(None))
        self.assertFalse(TransactionManager.validate_iban(12345))


class TestReadTransactionFromJson(unittest.TestCase):
    """Checks on reading and validating a request file."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manager = TransactionManager()

    def write(self, content):
        """Write `content` (dict or raw text) to a temporary file."""
        path = Path(self.tmp.name) / "request.json"
        path.write_text(content if isinstance(content, str) else json.dumps(content),
                        encoding="utf-8")
        return path

    def assert_error(self, path, message):
        """Assert that reading `path` fails with the given message."""
        with self.assertRaises(TransactionManagementException) as ctx:
            self.manager.read_transaction_from_json(path)
        self.assertEqual(ctx.exception.message, message)

    def test_valid_request(self):
        """A correct file returns a populated TransactionRequest."""
        path = self.write({"from": VALID_FROM, "to": VALID_TO, "receptor_name": "Jose Lopez"})
        request = self.manager.read_transaction_from_json(path)
        self.assertEqual(request.iban_from, VALID_FROM)
        self.assertEqual(request.iban_to, VALID_TO)
        self.assertEqual(request.receptor_name, "Jose Lopez")

    def test_missing_file(self):
        """A path that does not exist is reported."""
        self.assert_error(Path(self.tmp.name) / "nope.json", "Wrong file or file path")

    def test_malformed_json(self):
        """Text that is not JSON is reported."""
        self.assert_error(self.write("{not json"), "JSON Decode Error - Wrong JSON Format")

    def test_missing_key(self):
        """A missing key is reported."""
        path = self.write({"from": VALID_FROM, "to": VALID_TO})
        self.assert_error(path, "JSON Decode Error - Invalid JSON Key")

    def test_json_is_not_an_object(self):
        """A JSON list instead of an object is reported as an invalid key."""
        self.assert_error(self.write("[1, 2]"), "JSON Decode Error - Invalid JSON Key")

    def test_invalid_from_iban(self):
        """An invalid origin IBAN is reported."""
        path = self.write({"from": "ES0000", "to": VALID_TO, "receptor_name": "X"})
        self.assert_error(path, "Invalid FROM IBAN")

    def test_invalid_to_iban(self):
        """An invalid destination IBAN is reported."""
        path = self.write({"from": VALID_FROM, "to": "ES0000", "receptor_name": "X"})
        self.assert_error(path, "Invalid TO IBAN")


if __name__ == "__main__":
    unittest.main()
