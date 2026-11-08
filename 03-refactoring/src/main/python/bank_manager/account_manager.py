"""Account manager: transfers, deposits and balances."""
# pylint: disable=too-many-arguments
from bank_manager import AccountDeposit, TransferRequest
from bank_manager.iban_balance import IbanBalance
from bank_manager.storage.balances_json_store import BalancesJsonStore
from bank_manager.storage.deposits_json_store import DepositsJsonStore
from bank_manager.storage.transfer_json_store import TransfersJsonStore


class AccountManager:
    """Entry point for transfer requests, deposits and balance calculation."""
    @staticmethod
    def transfer_request(from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float)->str:
        """Validate a transfer, store it and return its transfer code."""
        my_request = TransferRequest(from_iban=from_iban,
                                     to_iban=to_iban,
                                     transfer_concept=concept,
                                     transfer_type=transfer_type,
                                     transfer_date=date,
                                     transfer_amount=amount)
        transfers_store = TransfersJsonStore()
        transfers_store.add_item(my_request)
        return my_request.transfer_code

    @staticmethod
    def deposit_into_account(input_file: str) -> str:
        """Read a deposit file, store the deposit and return its signature."""
        deposit_obj = AccountDeposit.load_deposit_from_file(input_file)
        deposits_json_store = DepositsJsonStore()
        deposits_json_store.add_item(deposit_obj)
        return deposit_obj.deposit_signature

    @staticmethod
    def calculate_balance(iban:str)->bool:
        """Calculate the balance of an IBAN and store it. Returns True on success."""
        iban_balance = IbanBalance(iban)
        balances_storage = BalancesJsonStore()
        balances_storage.add_item(iban_balance)
        return True
