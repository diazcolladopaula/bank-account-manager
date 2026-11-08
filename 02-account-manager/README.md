# Account Manager

`AccountManager` validates and stores transfer requests and deposits, and calculates account balances. Everything is persisted in JSON files.

This stage was developed test-first: the test cases were designed in a spreadsheet ([`docs/test_cases.xlsx`](docs/test_cases.xlsx), in Spanish) using equivalence classes and boundary values for the transfer fields, a syntax-based approach for the deposit files, and path coverage of the control-flow graph for the balance calculation. [`../03-refactoring`](../03-refactoring) restructures this code.

## Usage

```python
from bank_manager import AccountManager

manager = AccountManager(data_dir="data")   # JSON files are stored in ./data

code = manager.transfer_request(
    from_iban="ES6036390983922098113875",
    to_iban="ES9121000418450200051332",
    concept="Monthly rent",
    transfer_type="ORDINARY",
    date="01/01/2030",
    amount=500.0,
)
# `code` is the MD5 transfer code; the transfer is appended to data/transfers.json

signature = manager.deposit_into_account("deposit.json")   # SHA-256 signature
manager.calculate_balance("ES9121000418450200051332")      # writes data/<iban>.json
```

Every error is reported with an `AccountManagementException`; its `message` says what failed.

### Rules

| Operation | Input | Rules |
|---|---|---|
| `transfer_request` | `from_iban`, `to_iban` | Valid Spanish IBAN |
| | `concept` | 10 to 30 letters, digits or spaces, with at least one space |
| | `transfer_type` | `ORDINARY`, `URGENT` or `IMMEDIATE` |
| | `date` | `dd/mm/yyyy`, today or later, between 2025 and 2050 |
| | `amount` | From 10.00 to 10000.00 with at most two decimals |
| `deposit_into_account` | JSON file | Exactly the keys `IBAN` and `AMOUNT`, with a valid IBAN and an amount such as `"EUR 100.50"` greater than zero |
| `calculate_balance` | `iban` | Valid IBAN with at least one transaction in `data/all_transactions.json` |

A transfer identical to one already stored is rejected with `Duplicate transfer`.

## Tests

```bash
pip install freezegun
PYTHONPATH=src/main/python python -m unittest discover -s src/unittest/python -t src/unittest/python
```

The 61 tests use temporary folders, so they leave no files behind.

## Structure

```
src/main/python/bank_manager/
    account_manager.py                 Validation, transfers, deposits, balances
    transfer_request.py                Transfer data object and transfer code
    account_deposit.py                 Deposit data object and signature
    account_management_exception.py
src/unittest/python/                   Tests for each operation
docs/test_cases.xlsx                   Test case design
build.py, pylintrc, requirements.txt   PyBuilder and pylint configuration
```
