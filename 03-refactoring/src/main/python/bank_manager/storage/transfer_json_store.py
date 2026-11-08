"""Storage of transfers."""
# pylint: disable=too-few-public-methods
from bank_manager import AccountManagementException, TRANSFERS_STORE_FILE
from bank_manager.storage.json_store import JsonStore


class TransfersJsonStore(JsonStore):
    """JSON store for transfers; rejects duplicates."""
    _file_name = TRANSFERS_STORE_FILE

    def __init__(self):
        """Load the stored transfers."""
        super().__init__()

    def add_item(self, item):
        """Append a transfer unless an identical one is already stored."""
        self.load_list_from_file()
        for old_transfer in self._data_list:
            if old_transfer == item.to_json():
                raise AccountManagementException("Duplicated transfer in transfer list")
        super().add_item(item)
