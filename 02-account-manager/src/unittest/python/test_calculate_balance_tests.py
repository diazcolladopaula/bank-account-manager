"""Tests for AccountManager.calculate_balance (path labels refer to the control-flow graph)."""
import json
import tempfile
import unittest
from pathlib import Path

from bank_manager import AccountManager, AccountManagementException

TRANSACTIONS = [
    {"IBAN": "ES9121000418450200051332", "amount": "-500.00"},
    {"IBAN": "ES6036390983922098113875", "amount": "2500.50"},
    {"IBAN": "ES9121000418450200051332", "amount": "-800.06"},
    {"IBAN": "ES9121000418450200051332", "amount": "20.00"},
    {"IBAN": "ES6036390983922098113875", "amount": "-300.25"},
]


class TestCalculateBalance(unittest.TestCase):
    """Balance calculation from a transactions file."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data_dir = Path(tmp.name)
        self.write_transactions(TRANSACTIONS)
        self.manager = AccountManager(data_dir=self.data_dir)

    def write_transactions(self, content):
        """Write the transactions file used by the manager."""
        path = self.data_dir / "all_transactions.json"
        path.write_text(content if isinstance(content, str) else json.dumps(content),
                        encoding="utf-8")

    def read_balance(self, iban):
        """Read the balance file written for `iban`."""
        return json.loads((self.data_dir / f"{iban}.json").read_text(encoding="utf-8"))

    def assert_invalid_iban_code(self, iban):
        """calculate_balance must fail with InvalidIBANCode."""
        with self.assertRaises(AccountManagementException) as result:
            self.manager.calculate_balance(iban)
        self.assertEqual(result.exception.message, "InvalidIBANCode")

    def test_calculate_balance_ok_tc1(self):
        """1_2_3_5_10_11_10_14_16_17_18_19"""
        iban = "ES9121000418450200051332"
        self.assertTrue(self.manager.calculate_balance(iban))
        balance = self.read_balance(iban)
        self.assertEqual(balance["iban"], iban)
        self.assertIn("date", balance)
        self.assertAlmostEqual(balance["balance"], -1280.06)

    def test_calculate_balance_ok_tc2(self):
        """1_2_3_5_6_7_8_9_10_11_12_13_10_11_10_14_16_17_18_19"""
        iban = "ES6036390983922098113875"
        self.assertTrue(self.manager.calculate_balance(iban))
        self.assertAlmostEqual(self.read_balance(iban)["balance"], 2200.25)

    def test_calculate_balance_ko_tc3(self):
        """1_2_3_5_6_7_8_9_10_11_10_14_15"""
        self.assert_invalid_iban_code("ES7620770024003102575766")

    def test_calculate_balance_ko_tc4(self):
        """1_2_3_5_6_7_8_9_10_14_15"""
        self.assert_invalid_iban_code("ES9111112222333344445555")

    def test_calculate_balance_ko_tc5(self):
        """1_2_3_4"""
        self.assert_invalid_iban_code("ES00INVALID00000000000000")

    def test_calculate_balance_ko_tc6(self):
        """1_2_3_5_6_7_8_10_11_10_14_15"""
        self.assert_invalid_iban_code("ES9111112222333344445555")

    def test_calculate_balance_ko_tc7(self):
        """1_2_3_5_10: valid IBAN without transactions"""
        self.assert_invalid_iban_code("ES7921000813610123456789")

    def test_calculate_balance_ko_tc8(self):
        """1_2_3_5_10_11_10_14_15"""
        self.assert_invalid_iban_code("ES1234567890123456789012")

    def test_calculate_balance_ko_tc9(self):
        """1_2_3_5_10_14_15: wrong check digits"""
        self.assert_invalid_iban_code("ES7121000418450200051332")

    def test_calculate_balance_ko_tc10(self):
        """1_2_3_5_10_11_12_13_10_11_10_14_15: wrong check digits"""
        self.assert_invalid_iban_code("ES9521000418450200051332")

    def test_not_an_iban(self):
        """A value that is not a string is rejected."""
        self.assert_invalid_iban_code(None)

    def test_missing_transactions_file(self):
        """Without a transactions file no IBAN can have a balance."""
        (self.data_dir / "all_transactions.json").unlink()
        self.assert_invalid_iban_code("ES9121000418450200051332")

    def test_transactions_file_not_json(self):
        """A corrupted transactions file is reported."""
        self.write_transactions("not json")
        with self.assertRaises(AccountManagementException) as result:
            self.manager.calculate_balance("ES9121000418450200051332")
        self.assertEqual(result.exception.message, "File all_transactions is not a valid JSON")


if __name__ == "__main__":
    unittest.main()
