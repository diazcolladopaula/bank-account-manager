"""Deposit made into an account."""
from datetime import datetime, timezone
import hashlib

class AccountDeposit:
    """A deposit of money into an IBAN, signed with SHA-256."""

    def __init__(self,
                 to_iban: str,
                 deposit_amount):
        self.__alg = "SHA-256"
        self.__type = "DEPOSIT"
        self.__to_iban = to_iban
        self.__deposit_amount = deposit_amount
        justnow = datetime.now(timezone.utc)
        self.__deposit_date = datetime.timestamp(justnow)

    def to_json(self):
        """Return the deposit as a JSON-serialisable dict."""
        return {"alg": self.__alg,
                "type": self.__type,
                "to_iban": self.__to_iban,
                "deposit_amount": self.__deposit_amount,
                "deposit_date": self.__deposit_date,
                "deposit_signature": self.deposit_signature}

    def __signature_string(self):
        """Builds the string used to compute the deposit signature."""
        return "{alg:" + str(self.__alg) +",typ:" + str(self.__type) +",iban:" + \
               str(self.__to_iban) + ",amount:" + str(self.__deposit_amount) + \
               ",deposit_date:" + str(self.__deposit_date) + "}"

    @property
    def to_iban(self):
        """IBAN receiving the deposit."""
        return self.__to_iban

    @to_iban.setter
    def to_iban(self, value):
        self.__to_iban = value

    @property
    def deposit_amount(self):
        """Amount deposited."""
        return self.__deposit_amount
    @deposit_amount.setter
    def deposit_amount(self, value):
        self.__deposit_amount = value

    @property
    def deposit_date(self):
        """Timestamp of the deposit."""
        return self.__deposit_date
    @deposit_date.setter
    def deposit_date(self, value):
        self.__deposit_date = value

    @property
    def deposit_signature(self):
        """SHA-256 signature of the deposit data."""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()
