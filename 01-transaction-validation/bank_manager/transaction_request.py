"""Data object describing a transfer request."""
import json


class TransactionRequest:
    """Origin IBAN, destination IBAN and receiver name of a transfer."""

    def __init__(self, iban_from, iban_to, receptor_name):
        self.__iban_from = iban_from
        self.__iban_to = iban_to
        self.__receptor_name = receptor_name

    def __str__(self):
        return "TransactionRequest:" + json.dumps({
            "from": self.__iban_from,
            "to": self.__iban_to,
            "receptor_name": self.__receptor_name,
        })

    @property
    def iban_from(self):
        """IBAN of the origin account."""
        return self.__iban_from

    @iban_from.setter
    def iban_from(self, value):
        self.__iban_from = value

    @property
    def iban_to(self):
        """IBAN of the destination account."""
        return self.__iban_to

    @iban_to.setter
    def iban_to(self, value):
        self.__iban_to = value

    @property
    def receptor_name(self):
        """Name of the person receiving the transfer."""
        return self.__receptor_name

    @receptor_name.setter
    def receptor_name(self, value):
        self.__receptor_name = value
