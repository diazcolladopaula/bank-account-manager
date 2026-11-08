"""Spanish IBAN code."""
# pylint: disable=too-few-public-methods
from bank_manager import AccountManagementException
from bank_manager.data.attr.attribute import Attribute

class IbanCode(Attribute):
    """Spanish IBAN: "ES" followed by 22 digits, with correct mod-97 check digits."""
    def __init__(self, attr_value):
        super().__init__()
        self._validation_pattern = r"^ES[0-9]{22}"
        self._error_message = "Invalid IBAN format"
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        attr_value= super()._validate(attr_value)
        iban = attr_value
        original_code = iban[2:4]
        iban = iban[:2] + "00" + iban[4:]
        iban = iban[4:] + iban[:4]

        # Replace letters by numbers (A=10 ... Z=35)
        iban = (iban.replace('A', '10').replace('B', '11').
                replace('C', '12').replace('D', '13').replace('E', '14').
                replace('F', '15'))
        iban = (iban.replace('G', '16').replace('H', '17').
                replace('I', '18').replace('J', '19').replace('K', '20').
                replace('L', '21'))
        iban = (iban.replace('M', '22').replace('N', '23').
                replace('O', '24').replace('P', '25').replace('Q', '26').
                replace('R', '27'))
        iban = (iban.replace('S', '28').replace('T', '29').replace('U', '30').
                replace('V', '31').replace('W', '32').replace('X', '33'))
        iban = iban.replace('Y', '34').replace('Z', '35')

        # Convert to an integer
        iban_number = int(iban)
        # Remainder of the division by 97
        iban_mod_97 = iban_number % 97
        # Expected check digits: 98 minus the remainder
        control_digit = 98 - iban_mod_97
        if int(original_code) != control_digit:
            raise AccountManagementException("Invalid IBAN control digit")
        return attr_value
