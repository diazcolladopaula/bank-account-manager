# Account Manager (refactored)

The code of [`../02-account-manager`](../02-account-manager) restructured around two ideas:

- **Self-validating values.** Each field (IBAN, amount, date, concept, transfer type) is its own class. Creating the object validates the value, so an invalid field cannot reach the rest of the program.
- **Separate storage.** Reading and writing JSON files lives in a `storage` package instead of inside `AccountManager`, which is left with three short methods.

## Design

```
src/main/python/bank_manager/
    account_manager.py              transfer_request, deposit_into_account, calculate_balance
    transfer_request.py             Transfer built from validated attributes
    account_deposit.py              Deposit built from validated attributes
    iban_balance.py                 Balance of an IBAN
    data/attr/
        attribute.py                Base class: checks a value against a regular expression
        iban_code.py                IBAN, including the mod-97 check digits
        concept.py, transfer_type.py, transfer_date.py,
        transfer_amount.py, deposit_amount.py
    storage/
        json_store.py               Generic list of items kept in a JSON file
        transfer_json_store.py      Also rejects duplicated transfers
        deposits_json_store.py, balances_json_store.py
src/unittest/python/                Tests
src/unittest/JSONFiles/             Test data: input files, expected results and CSV test cases
```

`Attribute` is the base class. Each subclass sets a regular expression and an error message in its constructor, and `Attribute._validate` raises an `AccountManagementException` when the value does not match. `IbanCode` and `TransferDate` extend the check with extra rules (check digits, date range).

### Rules

| Value | Rule |
|---|---|
| IBAN | `ES` plus 22 digits, with correct check digits |
| Concept | 10 to 30 letters in at least two words separated by single spaces |
| Transfer type | `ORDINARY`, `INMEDIATE` or `URGENT` (spelled as in the assignment) |
| Transfer date | `dd/mm/yyyy`, today or later, between 2025 and 2050 |
| Transfer amount | From 10 to 10000 with at most two decimals |
| Deposit amount | Written as `EUR 0000.00`, greater than zero |

## Usage

```python
from bank_manager import AccountManager

code = AccountManager.transfer_request(
    from_iban="ES6211110783482828975098",
    to_iban="ES8658342044541216872704",
    concept="Monthly rent",
    transfer_type="ORDINARY",
    date="01/01/2030",
    amount=500.0,
)
```

Data files are written to `src/unittest/JSONFiles/` (see `account_management_config.py`). They are ignored by git.

## Tests

```bash
pip install freezegun
PYTHONPATH=src/main/python python -m unittest discover -s src/unittest/python -t src/unittest/python
```

The deposit and transfer tests are parametrised from the CSV files in `src/unittest/JSONFiles/`, where each row gives a case and its expected result. More than 70 JSON files in `deposits/` cover malformed inputs: a deleted, duplicated or modified character, field or key.
