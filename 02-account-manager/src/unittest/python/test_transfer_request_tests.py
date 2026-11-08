import json
import os
import tempfile
import unittest
from freezegun import freeze_time
from bank_manager import AccountManager, AccountManagementException

class TestTransferRequest(unittest.TestCase):
    """Tests for AccountManager.transfer_request."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.data_dir = tmp.name
    @freeze_time("2024-03-22")
    def test_transfer_request_ok_tc1(self):
        """Valid case"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Nomina marzo"
        amount_to_test = 10.00
        date_to_test = "01/01/2025"
        type_to_test = "ORDINARY"
        transfer_code = my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                                    concept=concept_to_test, amount=amount_to_test,
                                                    date=date_to_test, transfer_type=type_to_test)
        self.assertEqual(transfer_code, "d858beadbef5810335aca2a67c362a42")

    @freeze_time("2024-03-22")
    def test_transfer_request_ok_tc2(self):
        """Valid case"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Pago factura"
        amount_to_test = 10.01
        date_to_test = "2/2/2026"
        type_to_test = "URGENT"
        transfer_code = my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                                    concept=concept_to_test, amount=amount_to_test,
                                                    date=date_to_test, transfer_type=type_to_test)
        self.assertEqual(transfer_code, "37b3b65d436f749abe0f0d9d242cefd4")

    @freeze_time("2024-03-22")
    def test_transfer_request_ok_tc3(self):
        """Valid case"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Envio Internacional"
        amount_to_test = 10000.00
        date_to_test = "31/12/2050"
        type_to_test = "IMMEDIATE"
        transfer_code = my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                                    concept=concept_to_test, amount=amount_to_test,
                                                    date=date_to_test, transfer_type=type_to_test)
        self.assertEqual(transfer_code, "c4e4c952d9eb6c6b81cd4eec955fe6ce")

    @freeze_time("2024-03-22")
    def test_transfer_request_ok_tc4(self):
        """Valid case"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transferencia Pago Educacion"
        amount_to_test = 9999.99
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        transfer_code = my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                                    concept=concept_to_test, amount=amount_to_test,
                                                    date=date_to_test, transfer_type=type_to_test)
        self.assertEqual(transfer_code, "e1dc7427cf72b8905861de1efc288819")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc5(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = 5
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 9999.99
        date_to_test = "30/11/2049"
        type_to_test = "URGENT"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc6(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES9999999999999999999999"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 9999.99
        date_to_test = "30/11/2049"
        type_to_test = "URGENT"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc7(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES5674389475483473947883939"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc8(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES2357642374234823883"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc9(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "TM45393287654100123456789012"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc10(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "779121000418450200051332"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc11(self):
        """Invalid case: invalid from_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ESkelokekelokekelokekelo"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "from_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc12(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = 5
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc13(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9999999999999999999999"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc14(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES5674389475483473947883939"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc15(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES2357642374234823883"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc16(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "TM45393287654100123456789012"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc17(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "779121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc18(self):
        """Invalid case: invalid to_iban"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ESkelokekelokekelokekelo"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "to_iban not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc19(self):
        """Invalid case: invalid concept"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = 5
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "Invalid transfer concept")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc20(self):
        """Invalid case: invalid concept"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Este concepto sería muy largooo"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "Invalid transfer concept")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc21(self):
        """Invalid case: invalid concept"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "qwer tyui"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "Invalid transfer concept")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc22(self):
        """Invalid case: invalid concept"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "¿?=¡)¿?=¡)aa"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "Invalid transfer concept")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc23(self):
        """Invalid case: invalid concept"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "solounstring"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "Invalid transfer concept")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc24(self):
        """Invalid case: invalid transfer type"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = 5
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "transfer type is not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc25(self):
        """Invalid case: invalid transfer type"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2049"
        type_to_test = "URGE"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "transfer type is not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc26(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "almendra"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc27(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30112049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc28(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "32/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc29(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "00/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc30(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/00/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc31(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/13/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc32(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2051"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc33(self):
        """Invalid case: invalid date"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10.01
        date_to_test = "30/11/2024"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "date not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc34(self):
        """Invalid case: invalid amount"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = "Dinero"
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "amount not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc35(self):
        """Invalid case: invalid amount"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 10000.01
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "amount not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc36(self):
        """Invalid case: invalid amount"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 9.99
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "amount not valid")

    @freeze_time("2024-03-22")
    def test_transfer_request_tc37(self):
        """Invalid case: invalid amount"""
        my_manager = AccountManager(data_dir=self.data_dir)
        from_iban_to_test = "ES6036390983922098113875"
        to_iban_to_test = "ES9121000418450200051332"
        concept_to_test = "Transfer money now"
        amount_to_test = 9.575
        date_to_test = "30/11/2049"
        type_to_test = "ORDINARY"
        with self.assertRaises(Exception) as context:
            my_manager.transfer_request(from_iban=from_iban_to_test, to_iban=to_iban_to_test,
                                        concept=concept_to_test, amount=amount_to_test,
                                        date=date_to_test, transfer_type=type_to_test)

        self.assertEqual(str(context.exception), "amount not valid")


    @freeze_time("2024-03-22")
    def test_transfer_is_stored_with_correct_fields(self):
        """The stored record keeps each value in its own field."""
        manager = AccountManager(data_dir=self.data_dir)
        code = manager.transfer_request(from_iban="ES6036390983922098113875",
                                        to_iban="ES9121000418450200051332",
                                        concept="Nomina marzo", amount=10.0,
                                        date="01/01/2025", transfer_type="ORDINARY")
        with open(os.path.join(self.data_dir, "transfers.json"), encoding="utf-8") as file:
            stored = json.load(file)
        self.assertEqual(len(stored), 1)
        self.assertEqual(stored[0]["transfer_code"], code)
        self.assertEqual(stored[0]["from_iban"], "ES6036390983922098113875")
        self.assertEqual(stored[0]["to_iban"], "ES9121000418450200051332")
        self.assertEqual(stored[0]["transfer_type"], "ORDINARY")
        self.assertEqual(stored[0]["transfer_concept"], "Nomina marzo")

    @freeze_time("2024-03-22")
    def test_duplicate_transfer(self):
        """Sending the same transfer twice is rejected."""
        manager = AccountManager(data_dir=self.data_dir)
        arguments = {"from_iban": "ES6036390983922098113875",
                     "to_iban": "ES9121000418450200051332", "concept": "Nomina marzo",
                     "amount": 10.0, "date": "01/01/2025", "transfer_type": "ORDINARY"}
        manager.transfer_request(**arguments)
        with self.assertRaises(AccountManagementException) as context:
            manager.transfer_request(**arguments)
        self.assertEqual(context.exception.message, "Duplicate transfer")

    @freeze_time("2025-03-22 13:00:00")
    def test_transfer_date_today_is_valid(self):
        """A transfer dated today is accepted."""
        manager = AccountManager(data_dir=self.data_dir)
        code = manager.transfer_request(from_iban="ES6036390983922098113875",
                                        to_iban="ES9121000418450200051332",
                                        concept="Nomina marzo", amount=10.0,
                                        date="22/03/2025", transfer_type="ORDINARY")
        self.assertEqual(len(code), 32)


if __name__ == '__main__':
    unittest.main()
