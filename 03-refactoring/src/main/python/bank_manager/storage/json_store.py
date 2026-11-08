"""Generic JSON file storage."""
import json
from bank_manager import AccountManagementException


class JsonStore:
    """Keeps a list of items in a JSON file."""
    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def save_list_to_file(self):
        """Write the list to the file."""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise AccountManagementException("Wrong file or file path") from ex

    def load_list_from_file(self):
        """Read the list from the file (empty if the file does not exist)."""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise AccountManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def add_item(self, item):
        """Append an item to the store and save it."""
        self.load_list_from_file()
        self._data_list.append(item.to_json())
        self.save_list_to_file()
