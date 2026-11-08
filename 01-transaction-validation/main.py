"""Command-line demo: read a transfer request from a JSON file and validate it.

Usage: python main.py [path/to/request.json]
"""
import sys
from pathlib import Path

from bank_manager import TransactionManager, TransactionManagementException

DEFAULT_FILE = Path(__file__).resolve().parent / "sample_transaction.json"


def main():
    """Validate the given request file (or the bundled sample) and print it."""
    file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
    try:
        request = TransactionManager().read_transaction_from_json(file_path)
    except TransactionManagementException as error:
        print(f"Error: {error.message}")
        return 1
    print(request)
    print(f"IBAN_FROM: {request.iban_from}")
    print(f"IBAN_TO: {request.iban_to}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
