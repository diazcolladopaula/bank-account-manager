"""Custom exception raised when a transaction request is invalid."""


class TransactionManagementException(Exception):
    """Error raised while reading or validating a transaction request."""

    def __init__(self, message):
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """Human-readable description of the error."""
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value
