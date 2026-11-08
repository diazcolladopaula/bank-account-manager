"""Transfer request data object."""
import hashlib
import json
from datetime import datetime, timezone

from bank_manager.data.attr.concept import Concept
from bank_manager.data.attr.iban_code import IbanCode
from bank_manager.data.attr.transfer_amount import TransferAmount
from bank_manager.data.attr.transfer_date import TransferDate
from bank_manager.data.attr.transfer_type import TransferType


class TransferRequest:
    """A transfer between two IBAN, with every field validated on creation."""
    #pylint: disable=too-many-arguments
    def __init__(self,
                 from_iban: str,
                 transfer_type: str,
                 to_iban:str,
                 transfer_concept:str,
                 transfer_date:str,
                 transfer_amount:float):
        self.__from_iban = IbanCode(from_iban).value
        self.__to_iban = IbanCode(to_iban).value
        self.__transfer_type = TransferType(transfer_type).value
        self.__concept = Concept(transfer_concept).value
        self.__transfer_date = TransferDate(transfer_date).value
        self.__transfer_amount = TransferAmount(transfer_amount).value
        justnow = datetime.now(timezone.utc)
        self.__time_stamp = datetime.timestamp(justnow)

    def __str__(self):
        return "Transfer:" + json.dumps(self.__dict__)

    def to_json(self):
        """Return the transfer as a JSON-serialisable dict."""
        return {
            "from_iban": self.__from_iban,
            "to_iban": self.__to_iban,
            "transfer_type": self.__transfer_type,
            "transfer_amount": self.__transfer_amount,
            "transfer_concept": self.__concept,
            "transfer_date": self.__transfer_date,
            "time_stamp": self.__time_stamp,
            "transfer_code": self.transfer_code
        }
    @property
    def from_iban(self):
        """Sender's iban"""
        return self.__from_iban

    @from_iban.setter
    def from_iban(self, value):
        self.__from_iban = value

    @property
    def to_iban(self):
        """receiver's iban"""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def transfer_type(self):
        """Property representing the type of transfer: ORDINARY, INMEDIATE or URGENT"""
        return self.__transfer_type
    @transfer_type.setter
    def transfer_type(self, value):
        self.__transfer_type = value

    @property
    def transfer_amount(self):
        """Property representing the transfer amount"""
        return self.__transfer_amount
    @transfer_amount.setter
    def transfer_amount(self, value):
        self.__transfer_amount = value

    @property
    def transfer_concept(self):
        """Property representing the transfer concept"""
        return self.__concept
    @transfer_concept.setter
    def transfer_concept(self, value):
        self.__concept = value

    @property
    def transfer_date(self):
        """Property representing the transfer's date"""
        return self.__transfer_date
    @transfer_date.setter
    def transfer_date(self, value):
        self.__transfer_date = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def transfer_code(self):
        """MD5 signature of the transfer data, used as its code."""
        return hashlib.md5(str(self).encode()).hexdigest()
