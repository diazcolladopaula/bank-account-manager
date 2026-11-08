"""Exception raised by the account manager."""

class AccountManagementException(Exception):
    """Error raised when a request to the account manager is invalid."""
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
