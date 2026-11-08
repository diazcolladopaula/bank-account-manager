"""Storage of balances."""
from bank_manager import BALANCES_STORE_FILE
from bank_manager.storage.json_store import JsonStore


class BalancesJsonStore(JsonStore):
    """JSON store for balances."""
    _file_name = BALANCES_STORE_FILE
