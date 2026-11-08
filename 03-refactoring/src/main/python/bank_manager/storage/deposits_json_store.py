"""Storage of deposits."""
from bank_manager import DEPOSITS_STORE_FILE
from bank_manager.storage.json_store import JsonStore


# pylint: disable=too-few-public-methods

class DepositsJsonStore(JsonStore):
    """JSON store for deposits."""
    _file_name = DEPOSITS_STORE_FILE
