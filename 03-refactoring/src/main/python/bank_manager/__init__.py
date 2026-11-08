"""Bank account manager with validated value objects and JSON storage."""
from bank_manager.account_management_config import (JSON_FILES_PATH, JSON_FILES_DEPOSITS,
                                                  TRANSFERS_STORE_FILE, DEPOSITS_STORE_FILE,
                                                  TRANSACTIONS_STORE_FILE, BALANCES_STORE_FILE)
from bank_manager.account_management_exception import AccountManagementException
from bank_manager.account_deposit import AccountDeposit
from bank_manager.transfer_request import TransferRequest
from bank_manager.account_manager import AccountManager
